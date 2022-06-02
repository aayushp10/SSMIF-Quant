import { initializeConfig } from './utils/config';
import { initializeLogger } from './utils/logger';
import { initializeDB } from './db/connect';
import { runServer } from './server';

const main = async (): Promise<void> => {
  await initializeConfig();
  initializeLogger();
  initializeDB();
  await runServer();
};

if (require.main === module) {
  main().catch((err: Error) => {
    console.error(err.message);
    process.exit(1);
  });
}

export default main;
