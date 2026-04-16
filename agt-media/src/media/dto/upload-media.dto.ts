import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsOptional, IsString, IsUUID, IsIn } from 'class-validator';

export class UploadFileDto {
  @ApiPropertyOptional({ description: 'UUID proprietaire metier (users_auth.id)' })
  @IsOptional()
  @IsUUID()
  owner_user_id?: string;

  @ApiPropertyOptional({ enum: ['public', 'private'], default: 'public' })
  @IsOptional()
  @IsIn(['public', 'private'])
  visibility?: 'public' | 'private';

  @ApiPropertyOptional({ description: 'JSON des metadonnees cle-valeur. Ex: {"category":"profile"}' })
  @IsOptional()
  metadata?: any;
}

export class UploadFromUrlDto {
  @ApiProperty({ description: 'URL HTTP/HTTPS publique du fichier a importer' })
  @IsString()
  url: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsUUID()
  owner_user_id?: string;

  @ApiPropertyOptional({ enum: ['public', 'private'], default: 'public' })
  @IsOptional()
  @IsIn(['public', 'private'])
  visibility?: 'public' | 'private';

  @ApiPropertyOptional({ description: 'Metadonnees cle-valeur' })
  @IsOptional()
  metadata?: Record<string, string>;
}

export class UpdateMetadataDto {
  @ApiProperty({ description: 'Cle-valeur libres', example: { category: 'profile', source: 'mobile' } })
  metadata: Record<string, string>;
}

export class UpdateVisibilityDto {
  @ApiProperty({ enum: ['public', 'private'] })
  @IsIn(['public', 'private'])
  visibility: 'public' | 'private';
}
