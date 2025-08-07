interface User {
    id: number;
    name: string;
    username: string;
    email: string;
    address: {
        street: string;
        city: string;
    };
    phone: string;
    website: string;
    company: {
        name: string;
    };
}

interface Post {
    id: number;
    userId: number;
    title: string;
    body: string;
}

interface Comment {
    id: number;
    postId: number;
    name: string;
    email: string;
    body: string;
}

export interface QueryParameters {
    page: number;
    limit: number;
}

export interface PostWithUser extends Post {
    user: User;
    comments: Comment[];
}

export interface UserReportInterface {
    id: number;
    name: string;
    username: string;
    posts: Post[];
    comments: Comment[];
    posts_count: number;
    comments_count: number;
}