import { config } from 'dotenv';

export let debug = true;
export let production = true;
export let port = 3000;
export let websiteURL = 'https://quant.ssmif.com';
export let websiteHost = 'quant.ssmif.com';
export let dbConnectionURI: string;
export let jwtIssuer = 'ssmif';
export let jwtSecret: string;

export const initializeConfig = async (): Promise<void> => {
  config();
  if (process.env.DEBUG) {
    debug = process.env.DEBUG === 'true';
  }
  if (process.env.PRODUCTION) {
    production = process.env.PRODUCTION === 'true';
  }
  if (process.env.PORT) {
    const portNum = Number(process.env.PORT);
    if (!portNum) {
      throw new Error(`port ${process.env.PORT} is not a number`);
    }
    port = portNum.valueOf();
  }
  if (process.env.WEBSITE_URL) {
    websiteURL = process.env.WEBSITE_URL;
  }
  if (process.env.WEBSITE_HOST) {
    websiteHost = process.env.WEBSITE_HOST;
  }
  if (!process.env.DB_CONNECTION_URI) {
    throw new Error('no database uri provided');
  }
  dbConnectionURI = process.env.DB_CONNECTION_URI;
  if (process.env.JWT_ISSUER) {
    jwtIssuer = process.env.JWT_ISSUER;
  }
  if (!process.env.SECRET_KEY) {
    throw new Error('no jwt secret provided');
  }
  jwtSecret = process.env.SECRET_KEY;
};
