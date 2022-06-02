import { Path, GET } from 'typescript-rest';
import { RestReturnObj } from '../utils/returnObj';

@Path('/')
export class Index {
  @GET
  index(): RestReturnObj {
    return {
      message: 'go to /docs to view docs'
    };
  }
}
