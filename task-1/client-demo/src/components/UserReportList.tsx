import { useState, useEffect, useCallback } from 'react';
import { ChevronDown, ChevronUp, User, MessageSquare, FileText } from 'lucide-react';
import { fetchReports } from '../services/api_service';
import type { UserReportInterface } from '../types/interfaces';
// Import your actual service
// import { fetchReports } from 'your-service-path';


const UserReportsList = () => {
    const [reports, setReports] = useState<UserReportInterface[]>([]);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [expandedPosts, setExpandedPosts] = useState(new Set());
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);

    // Initial data load
    useEffect(() => {
        let mounted = true;

        const loadInitialReports = async () => {
            try {
                setLoading(true);
                //setError(null);

                const data = await fetchReports({
                    page: 1, limit: 10
                });


                if (mounted) {
                    setReports(data);
                    setHasMore(data.length === 10);
                    setPage(1);
                }
            } catch (err) {
                if (mounted) {
                    //setError(err || 'Failed to load reports');
                    console.error('Error loading initial reports:', err);
                }
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        };

        loadInitialReports();

        return () => {
            mounted = false;
        };
    }, []);

    // Load more data for infinite scroll
    const loadMoreReports = useCallback(async () => {
        if (loadingMore || !hasMore) return;

        try {
            setLoadingMore(true);
            //setError(null);

            const nextPage = page + 1;
            const data = await fetchReports({ page: nextPage, limit: 10 });

            setReports(prev => [...prev, ...data]);
            setHasMore(data.length === 10);
            setPage(nextPage);
        } catch (err) {
            //setError(err.message || 'Failed to load more reports');
            console.error('Error loading more reports:', err);
        } finally {
            setLoadingMore(false);
        }
    }, [page, loadingMore, hasMore]);

    // Scroll handler for infinite loading
    const handleScroll = useCallback((e: any) => {
        const { scrollTop, scrollHeight, clientHeight } = e.target;
        const threshold = scrollHeight - clientHeight * 1.2;

        if (scrollTop >= threshold && hasMore && !loadingMore) {
            loadMoreReports();
        }
    }, [hasMore, loadingMore, loadMoreReports]);

    // Toggle post expansion
    const togglePostExpansion = useCallback((postId: number) => {
        setExpandedPosts(prev => {
            const newSet = new Set(prev);
            if (newSet.has(postId)) {
                newSet.delete(postId);
            } else {
                newSet.add(postId);
            }
            return newSet;
        });
    }, []);

    // Get comments for a specific post
    const getCommentsForPost = useCallback((postId: number, comments: any) => {
        return comments?.filter((comment: { post_id: number; }) => comment.post_id === postId) || [];
    }, []);


    // Retry function
    const handleRetry = useCallback(() => {
        setReports([]);
        setPage(1);
        setHasMore(true);
        setExpandedPosts(new Set());
        //setError(null);

        // Trigger initial load effect
        window.location.reload();
    }, []);

    // Loading state
    if (loading) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <div className="flex items-center justify-center min-h-64">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                        <div className="text-gray-600 text-lg">Loading reports...</div>
                    </div>
                </div>
            </div>
        );
    }

    // Error state
    if (reports.length === 0) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <div className="flex items-center justify-center min-h-64 bg-red-50 rounded-lg">
                    <div className="text-center">
                        <div className="text-red-600 text-lg font-semibold mb-2">Error</div>
                        <button
                            onClick={handleRetry}
                            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                        >
                            Try Again
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // Empty state
    if (!loading && reports.length === 0) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <div className="flex items-center justify-center min-h-64 bg-gray-50 rounded-lg">
                    <div className="text-center">
                        <User className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                        <div className="text-gray-600 text-lg font-medium mb-2">No Reports Found</div>
                        <div className="text-gray-500">There are no user reports to display at the moment.</div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto p-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">User Reports</h1>

            <div
                className="space-y-6 max-h-screen overflow-y-auto pr-2"
                onScroll={handleScroll}
            >
                {reports.map((user) => (
                    <div key={user.id} className="bg-white rounded-xl shadow-lg border border-gray-200">
                        {/* User Header */}
                        <div className="p-6 border-b border-gray-100">
                            <div className="flex items-center space-x-4">
                                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                    <User className="w-6 h-6 text-white" />
                                </div>
                                <div className="flex-1">
                                    <h2 className="text-xl font-bold text-gray-900">{user.name}</h2>
                                    <p className="text-gray-600">@{user.username}</p>
                                </div>
                                <div className="flex space-x-6 text-sm text-gray-500">
                                    <div className="flex items-center space-x-1">
                                        <FileText className="w-4 h-4" />
                                        <span>{user.posts_count || 0} posts</span>
                                    </div>
                                    <div className="flex items-center space-x-1">
                                        <MessageSquare className="w-4 h-4" />
                                        <span>{user.comments_count || 0} comments</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Posts */}
                        <div className="p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Posts</h3>

                            {!user.posts || user.posts.length === 0 ? (
                                <div className="text-center py-8 text-gray-500">
                                    No posts available for this user
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {user.posts.map((post) => {
                                        const isExpanded = expandedPosts.has(post.id);
                                        const postComments = getCommentsForPost(post.id, user.comments);

                                        return (
                                            <div key={post.id} className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                                                {/* Post Header */}
                                                <div
                                                    className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                                                    onClick={() => togglePostExpansion(post.id)}
                                                >
                                                    <div className="flex items-center justify-between">
                                                        <div className="flex-1">
                                                            <h4 className="font-semibold text-gray-900 mb-1">
                                                                {post.title || 'Untitled Post'}
                                                            </h4>

                                                        </div>
                                                        <div className="flex items-center space-x-2">
                                                            {postComments.length > 0 && (
                                                                <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                                                                    {postComments.length} comments
                                                                </span>
                                                            )}
                                                            {isExpanded ? (
                                                                <ChevronUp className="w-5 h-5 text-gray-400" />
                                                            ) : (
                                                                <ChevronDown className="w-5 h-5 text-gray-400" />
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* Expandable Content */}
                                                {isExpanded && (
                                                    <div className="border-t border-gray-100">
                                                        {/* Post Content */}
                                                        {post.body && (
                                                            <div className="p-4 bg-gray-50">
                                                                <p className="text-gray-700 leading-relaxed">{post.body}</p>
                                                            </div>
                                                        )}

                                                        {/* Comments */}
                                                        {postComments.length > 0 && (
                                                            <div className="p-4">
                                                                <h5 className="font-medium text-gray-900 mb-3">Comments</h5>
                                                                <div className="space-y-3">
                                                                    {postComments.map((comment: any) => (
                                                                        <div key={comment.id} className="bg-gray-50 rounded-lg p-3">
                                                                            <p className="text-gray-700 mb-1">{comment.content}</p>

                                                                        </div>
                                                                    ))}
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {/* Loading More Spinner */}
                {loadingMore && (
                    <div className="flex justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                    </div>
                )}

                {/* Error while loading more */}
                {reports.length > 0 && (
                    <div className="text-center py-4">
                        <button
                            onClick={loadMoreReports}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            Try Again
                        </button>
                    </div>
                )}

                {/* End of Data Message */}
                {!hasMore && !loadingMore && reports.length > 0 && (
                    <div className="text-center py-8 text-gray-500">
                        No more reports to load
                    </div>
                )}
            </div>
        </div>
    );
};

export default UserReportsList;