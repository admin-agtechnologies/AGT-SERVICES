import { SetMetadata } from '@nestjs/common';
import { IS_PUBLIC_KEY } from './jwt-auth.guard';

/** Marque un endpoint comme public (pas de JWT requis) */
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
