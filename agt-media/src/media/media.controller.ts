/**
 * MediaController -- exposition de tous les endpoints REST.
 * Prefixe global : /api/v1 (configure dans main.ts)
 * Controller monte sur : media
 * Resultat : /api/v1/media/*
 * CDC Media v1.4 -- sections 9.1 a 9.6.
 */
import {
  Controller,
  Post,
  Get,
  Put,
  Delete,
  Param,
  Query,
  Body,
  UploadedFile,
  UploadedFiles,
  UseInterceptors,
  UseGuards,
  Req,
  Res,
  ParseUUIDPipe,
  DefaultValuePipe,
  ParseIntPipe,
  ParseBoolPipe,
  HttpCode,
  HttpStatus,
  BadRequestException,
} from '@nestjs/common';
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';
import {
  ApiTags,
  ApiOperation,
  ApiBearerAuth,
  ApiConsumes,
  ApiBody,
  ApiQuery,
  ApiParam,
} from '@nestjs/swagger';
import { Response, Request } from 'express';
import { MediaService } from './media.service';
import { JwtAuthGuard } from '../common/auth/jwt-auth.guard';
import { S2SGuard } from '../common/auth/s2s.guard';
import { Public } from '../common/auth/public.decorator';
import {
  UploadFileDto,
  UploadFromUrlDto,
  UpdateMetadataDto,
  UpdateVisibilityDto,
} from './dto/upload-media.dto';
import * as crypto from 'crypto';
import { ConfigService } from '@nestjs/config';

@ApiTags('Upload', 'Consultation', 'Gestion', 'RGPD', 'Statistiques')
@ApiBearerAuth('BearerAuth')
@UseGuards(JwtAuthGuard)
@Controller('media')
export class MediaController {
  constructor(
    private readonly mediaService: MediaService,
    private readonly config: ConfigService,
  ) {}

  // ============================================================
  // UPLOAD  CDC 9.2
  // ============================================================

  /**
   * POST /api/v1/media
   * Upload fichier unique. CDC 9.2.1.
   * Retourne url si public, signed_url si private.
   */
  @Post()
  @ApiOperation({ summary: 'Upload fichier unique (multipart/form-data)' })
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        file: { type: 'string', format: 'binary' },
        visibility: { type: 'string', enum: ['public', 'private'], default: 'public' },
        owner_user_id: { type: 'string', format: 'uuid' },
        metadata: { type: 'string', description: 'JSON stringify des metadonnees cle-valeur' },
      },
      required: ['file'],
    },
  })
  @UseInterceptors(FileInterceptor('file', { limits: { fileSize: 52_428_800 } }))
  async upload(
    @UploadedFile() file: Express.Multer.File,
    @Body() dto: UploadFileDto,
    @Req() req: Request & { auth: any },
  ) {
    if (!file) throw new BadRequestException('Fichier requis (champ "file")');

    const platformId = req.auth?.platform_id || req.auth?.sub;
    const uploadedBy = req.auth?.is_s2s ? null : (req.auth?.id || req.auth?.sub);

    let metadata: Record<string, string> | undefined;
    if (dto.metadata) {
      try {
        metadata = typeof dto.metadata === 'string' ? JSON.parse(dto.metadata) : dto.metadata;
      } catch {
        throw new BadRequestException('metadata doit etre un JSON valide');
      }
    }

    const result = await this.mediaService.uploadFile(
      file,
      platformId,
      uploadedBy,
      dto.owner_user_id || null,
      dto.visibility || 'public',
      metadata,
    );

    return { success: true, data: result };
  }

  /**
   * POST /api/v1/media/batch
   * Upload multiple (max 10). CDC 9.2.2. Reponse 207 Multi-Status.
   */
  @Post('batch')
  @HttpCode(207)
  @ApiOperation({ summary: 'Upload multiple (max 10 fichiers) -- reponse 207' })
  @ApiConsumes('multipart/form-data')
  @UseInterceptors(FilesInterceptor('files', 10, { limits: { fileSize: 52_428_800 } }))
  async uploadBatch(
    @UploadedFiles() files: Express.Multer.File[],
    @Body() dto: UploadFileDto,
    @Req() req: Request & { auth: any },
  ) {
    if (!files || files.length === 0) throw new BadRequestException('Au moins un fichier requis (champ "files")');

    const platformId = req.auth?.platform_id || req.auth?.sub;
    const uploadedBy = req.auth?.is_s2s ? null : (req.auth?.id || req.auth?.sub);

    const results = await Promise.allSettled(
      files.map((file) =>
        this.mediaService.uploadFile(
          file, platformId, uploadedBy,
          dto.owner_user_id || null, dto.visibility || 'public',
        ),
      ),
    );

    return {
      results: results.map((r) =>
        r.status === 'fulfilled'
          ? { status: 201, data: r.value }
          : { status: 422, error: r.reason?.message || 'Erreur inconnue' },
      ),
    };
  }

  /**
   * POST /api/v1/media/from-url
   * Import depuis URL externe. CDC 9.2.3. SSRF complet.
   */
  @Post('from-url')
  @ApiOperation({ summary: 'Importe un fichier depuis URL externe (SSRF protege)' })
  async uploadFromUrl(
    @Body() dto: UploadFromUrlDto,
    @Req() req: Request & { auth: any },
  ) {
    const platformId = req.auth?.platform_id || req.auth?.sub;
    const uploadedBy = req.auth?.is_s2s ? null : (req.auth?.id || req.auth?.sub);

    const result = await this.mediaService.uploadFromUrl(
      dto.url,
      platformId,
      uploadedBy,
      dto.owner_user_id || null,
      dto.visibility || 'public',
      dto.metadata,
    );

    return { success: true, data: result };
  }

  // ============================================================
  // CONSULTATION  CDC 9.3
  // NOTE : les routes statiques DOIVENT etre declarees AVANT :id
  // pour eviter les conflits de routage Express.
  // ============================================================

  /**
   * GET /api/v1/media/stats
   * Statistiques globales. CDC 9.6.1.
   */
  @Get('stats')
  @ApiOperation({ summary: 'Statistiques globales des medias' })
  async getStats() {
    return this.mediaService.getStats();
  }

  /**
   * GET /api/v1/media/stats/:platformId
   * Statistiques par plateforme. CDC 9.6.2.
   */
  @Get('stats/:platformId')
  @ApiOperation({ summary: 'Statistiques par plateforme' })
  async getStatsByPlatform(@Param('platformId', ParseUUIDPipe) platformId: string) {
    return this.mediaService.getStats(platformId);
  }

  /**
   * GET /api/v1/media
   * Listage pagine avec tous les filtres CDC. CDC 9.3.6.
   * Query : platform_id, uploaded_by, owner_user_id, mime_type, visibility, from, to, page, limit.
   */
  @Get()
  @ApiOperation({ summary: 'Liste paginee des medias avec filtres' })
  @ApiQuery({ name: 'platform_id', required: false })
  @ApiQuery({ name: 'uploaded_by', required: false })
  @ApiQuery({ name: 'owner_user_id', required: false })
  @ApiQuery({ name: 'mime_type', required: false })
  @ApiQuery({ name: 'visibility', required: false, enum: ['public', 'private'] })
  @ApiQuery({ name: 'from', required: false, description: 'Date ISO8601' })
  @ApiQuery({ name: 'to', required: false, description: 'Date ISO8601' })
  @ApiQuery({ name: 'page', required: false, type: Number })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  async list(
    @Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number,
    @Query('limit', new DefaultValuePipe(20), ParseIntPipe) limit: number,
    @Query('platform_id') platform_id?: string,
    @Query('uploaded_by') uploaded_by?: string,
    @Query('owner_user_id') owner_user_id?: string,
    @Query('mime_type') mime_type?: string,
    @Query('visibility') visibility?: string,
    @Query('from') from?: string,
    @Query('to') to?: string,
  ) {
    return this.mediaService.listMedia(page, Math.min(limit, 100), {
      platform_id, uploaded_by, owner_user_id, mime_type, visibility, from, to,
    });
  }

  /**
   * GET /api/v1/media/:id/info
   * Metadonnees uniquement. CDC 9.3.2.
   */
  @Get(':id/info')
  @ApiOperation({ summary: 'Metadonnees completes (JSON) d un fichier' })
  async getInfo(@Param('id', ParseUUIDPipe) id: string) {
    const media = await this.mediaService.getMediaInfo(id);
    return { success: true, data: media };
  }

  /**
   * GET /api/v1/media/:id/thumbnails
   * Liste des variantes thumbnails. CDC 9.3.3.
   */
  @Get(':id/thumbnails')
  @ApiOperation({ summary: 'Liste des thumbnails d un fichier' })
  async getThumbnails(@Param('id', ParseUUIDPipe) id: string) {
    const variants = await this.mediaService.getVariants(id);
    return { success: true, data: variants.filter((v) => v.variant_type === 'thumbnail') };
  }

  /**
   * GET /api/v1/media/:id/thumbnail/:size
   * Thumbnail specifique (ex: 300x300). CDC 9.3.4.
   */
  @Get(':id/thumbnail/:size')
  @ApiOperation({ summary: 'Thumbnail specifique par taille (ex: 300x300)' })
  async getThumbnailBySize(
    @Param('id', ParseUUIDPipe) id: string,
    @Param('size') size: string,
    @Res() res: Response,
  ) {
    // Valider le format "WxH"
    if (!/^\d+x\d+$/.test(size)) {
      throw new BadRequestException('Format de taille invalide. Utiliser WxH (ex: 300x300)');
    }
    const { buffer, mimeType } = await this.mediaService.getThumbnailBySize(id, size);
    res.set({ 'Content-Type': mimeType, 'Content-Length': buffer.length });
    res.send(buffer);
  }

  /**
   * GET /api/v1/media/:id/resize
   * Resize a la volee. CDC 9.3.5. Query: w, h, crop. Cache Redis.
   */
  @Get(':id/resize')
  @ApiOperation({ summary: 'Resize a la volee (cache Redis). Query: w, h, crop' })
  @ApiQuery({ name: 'w', required: true, type: Number, description: 'Largeur cible en px' })
  @ApiQuery({ name: 'h', required: true, type: Number, description: 'Hauteur cible en px' })
  @ApiQuery({ name: 'crop', required: false, type: Boolean, description: 'Recadrer (true) ou conserver les proportions (false)' })
  async resize(
    @Param('id', ParseUUIDPipe) id: string,
    @Query('w', ParseIntPipe) w: number,
    @Query('h', ParseIntPipe) h: number,
    @Query('crop', new DefaultValuePipe(false), ParseBoolPipe) crop: boolean,
    @Res() res: Response,
  ) {
    if (w < 1 || w > 4000 || h < 1 || h > 4000) {
      throw new BadRequestException('Dimensions invalides (1-4000px)');
    }
    const { buffer, mimeType } = await this.mediaService.resizeOnTheFly(id, w, h, crop);
    res.set({
      'Content-Type': mimeType,
      'Content-Length': buffer.length,
      'Cache-Control': 'public, max-age=3600',
    });
    res.send(buffer);
  }

  /**
   * GET /api/v1/media/:id/signed-url
   * URL temporaire signee. CDC 9.4.5.
   */
  @Get(':id/signed-url')
  @ApiOperation({ summary: 'Genere une URL signee temporaire' })
  @ApiQuery({ name: 'expires', required: false, description: 'TTL en secondes (defaut: 3600)' })
  async getSignedUrl(
    @Param('id', ParseUUIDPipe) id: string,
    @Query('expires', new DefaultValuePipe(3600), ParseIntPipe) expires: number,
    @Req() req: Request & { auth: any },
  ) {
    const url = await this.mediaService.generateSignedUrl(id, req.auth, expires);
    return { success: true, data: { signed_url: url, expires_in: expires } };
  }

  /**
   * GET /api/v1/media/:id/access-logs
   * Logs d acces pagines. CDC 9.3.7.
   */
  @Get(':id/access-logs')
  @ApiOperation({ summary: 'Logs d acces d un fichier (admin/proprietaire)' })
  @ApiQuery({ name: 'page', required: false, type: Number })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  async getAccessLogs(
    @Param('id', ParseUUIDPipe) id: string,
    @Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number,
    @Query('limit', new DefaultValuePipe(50), ParseIntPipe) limit: number,
  ) {
    return this.mediaService.getAccessLogs(id, page, limit);
  }

  /**
   * GET /api/v1/media/:id/serve?sig=...&exp=...
   * Sert un fichier via URL signee (endpoint public). CDC 9.4.5.
   */
  @Public()
  @Get(':id/serve')
  @ApiOperation({ summary: 'Acces fichier via URL signee (public, token temporaire)' })
  async serveSignedUrl(
    @Param('id', ParseUUIDPipe) id: string,
    @Query('sig') sig: string,
    @Query('exp') exp: string,
    @Res() res: Response,
  ) {
    const expiry = parseInt(exp || '0');
    if (!sig || !exp) return res.status(400).json({ error: 'Parametres sig et exp requis' });
    if (Date.now() / 1000 > expiry) return res.status(410).json({ error: 'URL expiree' });

    const secret = this.config.get<string>('SIGNED_URL_SECRET', 'change-me-secret');
    const expected = crypto.createHmac('sha256', secret).update(`${id}:${expiry}`).digest('hex');
    if (sig !== expected) return res.status(403).json({ error: 'Signature invalide' });

    const { buffer, mimeType, filename } = await this.mediaService.downloadFile(id, { is_s2s: true }, undefined);
    res.set({ 'Content-Type': mimeType, 'Content-Disposition': `inline; filename="${filename}"` });
    res.send(buffer);
  }

  /**
   * GET /api/v1/media/:id
   * Telechargement binaire. CDC 9.3.1. Declenche log d acces.
   */
  @Get(':id')
  @ApiOperation({ summary: 'Telechargement binaire du fichier brut' })
  async download(
    @Param('id', ParseUUIDPipe) id: string,
    @Req() req: Request & { auth: any },
    @Res() res: Response,
  ) {
    const ip = (req.headers['x-forwarded-for'] as string) || req.ip;
    const { buffer, mimeType, filename } = await this.mediaService.downloadFile(id, req.auth, ip);
    res.set({
      'Content-Type': mimeType,
      'Content-Disposition': `inline; filename="${encodeURIComponent(filename)}"`,
      'Content-Length': buffer.length,
    });
    res.send(buffer);
  }

  // ============================================================
  // GESTION  CDC 9.4
  // ============================================================

  /**
   * PUT /api/v1/media/:id/metadata
   * MAJ metadonnees personnalisees. CDC 9.4.1.
   */
  @Put(':id/metadata')
  @ApiOperation({ summary: 'Met a jour les metadonnees custom (cle-valeur)' })
  async updateMetadata(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: UpdateMetadataDto,
    @Req() req: Request & { auth: any },
  ) {
    const media = await this.mediaService.updateMetadata(id, dto.metadata, req.auth);
    return { success: true, data: media };
  }

  /**
   * PUT /api/v1/media/:id/visibility
   * Changement de visibilite. CDC 9.4.2.
   */
  @Put(':id/visibility')
  @ApiOperation({ summary: 'Change la visibilite d un fichier (public/private)' })
  async updateVisibility(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: UpdateVisibilityDto,
    @Req() req: Request & { auth: any },
  ) {
    const media = await this.mediaService.updateVisibility(id, dto.visibility, req.auth);
    return { success: true, data: media };
  }

  /**
   * DELETE /api/v1/media/:id
   * Soft delete. CDC 9.4.3. Reponse 204.
   */
  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Soft delete (marque deleted_at)' })
  async softDelete(
    @Param('id', ParseUUIDPipe) id: string,
    @Req() req: Request & { auth: any },
  ) {
    await this.mediaService.softDelete(id, req.auth);
  }

  /**
   * DELETE /api/v1/media/:id/permanent
   * Hard delete -- S2S uniquement. CDC 9.4.4. Reponse 204.
   */
  @Delete(':id/permanent')
  @UseGuards(S2SGuard)
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Hard delete permanent -- token S2S uniquement' })
  async hardDelete(@Param('id', ParseUUIDPipe) id: string) {
    await this.mediaService.hardDelete(id);
  }

  /**
   * DELETE /api/v1/media/by-user/:userId
   * Purge RGPD totale. CDC 9.4.6. S2S uniquement.
   * Retourne files_deleted, variants_deleted, storage_freed_bytes.
   */
  @Delete('by-user/:userId')
  @UseGuards(S2SGuard)
  @ApiOperation({ summary: 'Purge RGPD -- suppression totale fichiers utilisateur (S2S)' })
  async purgeByUser(@Param('userId', ParseUUIDPipe) userId: string) {
    return this.mediaService.purgeByUser(userId);
  }
}
