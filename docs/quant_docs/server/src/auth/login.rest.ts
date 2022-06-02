import { Path, POST, ContextResponse, Errors } from 'typescript-rest';
import { Response } from 'express';
import { RestReturnObj } from '../utils/returnObj';
import { jwtIssuer, jwtSecret, production } from '../utils/config';
import { getRepository, FindOneOptions } from 'typeorm';
import User from '../utils/user.entity';
import argon2 from 'argon2';
import { sign, SignOptions } from 'jsonwebtoken';
import { authCookieName, JWTAuthData } from './auth';

const accessJWTExpiration = '2h';

interface LoginData {
  usernameEmail: string;
  password: string;
}

export const generateJWTAccess = (user: User): Promise<string> => {
  return new Promise(async (resolve, reject) => {
    const authData: JWTAuthData = {
      id: user.id,
      user_type: user.user_type
    };
    const signOptions: SignOptions = {
      issuer: jwtIssuer,
      expiresIn: accessJWTExpiration
    };
    sign(authData, jwtSecret, signOptions, (err, token) => {
      if (err) {
        reject(err as Error);
      } else {
        resolve(token as string);
      }
    });
  });
};

@Path('/api/login')
export class Login {
  @POST
  async login(@ContextResponse res: Response, loginData: LoginData): Promise<RestReturnObj> {
    if (!loginData.usernameEmail) {
      throw new Errors.BadRequestError('no username / email provided');
    }
    if (!loginData.password) {
      throw new Errors.BadRequestError('no password provided');
    }
    const UserModel = getRepository(User);
    const findOptions: FindOneOptions<User> = {
      select: ['id', 'user_type', 'password']
    };
    let user: User;
    if (loginData.usernameEmail.includes('@')) {
      const userRes = await UserModel.findOne({
        email: loginData.usernameEmail
      }, findOptions);
      if (!userRes) {
        throw new Error(`cannot find user with email ${loginData.usernameEmail}`);
      }
      user = userRes as User;
    } else {
      const userRes = await UserModel.findOne({
        username: loginData.usernameEmail
      }, findOptions);
      if (!userRes) {
        throw new Error(`cannot find user with username ${loginData.usernameEmail}`);
      }
      user = userRes as User;
    }
    if (!await argon2.verify(user.password, loginData.password)) {
      throw new Errors.BadRequestError('password is invalid');
    }
    const token = await generateJWTAccess(user);
    res.cookie(authCookieName, token, {
      httpOnly: true,
      secure: production,
      sameSite: production ? 'strict' : 'lax',
      signed: true
    });
    return {
      message: 'login successful'
    };
  }
}
