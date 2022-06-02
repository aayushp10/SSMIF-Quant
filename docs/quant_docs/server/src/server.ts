import { connectLogger, getLogger } from 'log4js';
import { jwtSecret, port, production, websiteHost, websiteURL } from './utils/config';
import { createServer } from 'http';
import express from 'express';
import { Server, Errors } from 'typescript-rest';
import cors, { CorsOptions } from 'cors';
import cookieParser from 'cookie-parser';
import statusMonitor from 'express-status-monitor';
import bodyParser from 'body-parser';
import compression from 'compression';
import { join } from 'path';
import httpStatusCodes from 'http-status-codes';
import { authMiddleware } from './auth/auth';

const logger = getLogger();

const errorHandler = (err: any, _req: express.Request, res: express.Response, next: express.NextFunction): void => {
  if (err instanceof Errors.HttpError) {
    logger.info('found an error');
    if (res.headersSent) { // important to sallow default error handler to close connection if headers already sent
      return next(err);
    }
    res.set('Content-Type', 'application/json');
    res.status(err.statusCode);
    res.json({ error: err.message, code: err.statusCode });
  } else {
    next(err);
  }
};

export const runServer = async (): Promise<void> => {
  // build the server
  const app = express();
  const corsConfig: CorsOptions = {
    credentials: true,
    origin: [websiteURL]
  };
  app.use(cors(corsConfig));
  app.use(cookieParser(jwtSecret));
  // use in proxy that you trust (like aws)
  // see http://expressjs.com/en/guide/behind-proxies.html
  app.set('trust proxy', true);
  app.use(connectLogger(logger, {}));
  app.use(compression());
  // web status monitor page
  app.use(statusMonitor({
    path: '/status',
    healthChecks: [{
      host: 'localhost',
      path: '/',
      port,
      protocol: 'http'
    }]
  }));
  app.use(bodyParser.urlencoded({
    extended: true
  }));
  app.use(bodyParser.json());

  app.get('/', (_req: express.Request, res: express.Response) => {
    res.status(httpStatusCodes.MOVED_TEMPORARILY).redirect('/docs');
  });

  Server.buildServices(app);
  Server.loadServices(app, '**/*.rest.{ts,js}', __dirname);
  const swaggerSchemes = [];
  let swaggerHost = `localhost:${port}`;
  if (production) {
    swaggerSchemes.push('https');
    swaggerHost = websiteHost;
  }
  swaggerSchemes.push('http');
  Server.swagger(app, {
    endpoint: 'swagger',
    filePath: join(__dirname, '../swagger.yml'),
    host: swaggerHost,
    schemes: swaggerSchemes
  });

  // error handler for rest requests
  app.use(errorHandler);

  app.use('/docs', authMiddleware);
  app.use('/docs', express.static('static'));
  app.use(express.static('public', {
    extensions: ['html', 'htm']
  }));

  const httpServer = createServer(app);
  httpServer.listen(port, () => logger.info(`Docs server started: http://localhost:${port} 🚀`));
};
