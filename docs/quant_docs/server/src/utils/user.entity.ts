import { Entity, PrimaryGeneratedColumn, Column, Index } from 'typeorm';
import { IsDefined } from 'class-validator';

// must match peewee and sdk
export enum UserType {
  quant = 'quant',
  equity = 'equity',
  senior_management = 'senior_management',
}

// note - this must match the peewee model in the sdk
@Entity({ name: 'users' })
export default class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'text' })
  @Index({ unique: true })
  @IsDefined()
  email: string;

  @Column({ type: 'text' })
  @Index({ unique: true })
  @IsDefined()
  username: string;

  @Column({ type: 'text' })
  @IsDefined()
  name: string;

  @Column({ type: 'text' })
  @IsDefined()
  password: string;

  @Column({ type: 'boolean' })
  @IsDefined()
  receives_weekly_report: boolean;

  // note - needs to be text because enums aren't supported in peewee
  // right now we're using a text field to represent an enum and coverting manually
  // see this: https://github.com/coleifer/peewee/issues/630
  // note tbe samples use text instead of enum for the fields
  @Column({ type: 'text', enum: UserType })
  @IsDefined()
  user_type: UserType;
}
