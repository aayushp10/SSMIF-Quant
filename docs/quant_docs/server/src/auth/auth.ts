import { jwtSecret } from '../utils/config';
import express from 'express';
import { UserType } from '../utils/user.entity';
import { verify } from 'jsonwebtoken';

const unauthenticatedPaths: string[] = [];

export const authCookieName = 'authCookie';

export interface JWTAuthData {
  id: string;
  user_type: UserType;
}

export const decodeAuth = (token: string): Promise<JWTAuthData> => {
  return new Promise((resolve, reject) => {
    try {
      verify(token, jwtSecret, {
        algorithms: ['HS256']
      }, async (err, res: any) => {
        try {
          if (err) {
            throw err as Error;
          }
          const data = res as JWTAuthData;
          resolve(data);
        } catch (err) {
          const errObj = err as Error;
          reject(errObj);
        }
      });
    } catch (err) {
      const errObj = err as Error;
      reject(errObj);
    }
  });
};

export const authMiddleware = async (req: express.Request, res: express.Response, next: express.NextFunction): Promise<void> => {
  if (unauthenticatedPaths.includes(req.path)) {
    next();
    return;
  }
  try {
    if (!(authCookieName in req.signedCookies)) {
      throw new Error('cannot find cookie');
    }
    await decodeAuth(req.signedCookies[authCookieName]);
    next();
  } catch (err) {
    res.redirect('/login');
    return;
  }
};
