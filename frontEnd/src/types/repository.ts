export interface Repository {
  id: string;
  title: string;
  description: string;
  url: string;
  tags: string[];
  createdAt: Date;
}

export interface RepositoryFormData {
  title: string;
  description: string;
  url: string;
  tags: string;
}