/**
 * User profile page
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { reviewsAPI } from '../services/api';
import './Profile.css';

const Profile = () => {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
      return;
    }
    if (user) {
      loadReviews();
    }
  }, [user, authLoading, navigate]);

  const loadReviews = async () => {
    try {
      const response = await reviewsAPI.list();
      setReviews(response.data.filter((r) => r.user_id === user.id));
    } catch (error) {
      console.error('Failed to load reviews:', error);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || loading) {
    return <div className="loading">Loading profile...</div>;
  }

  if (!user) {
    return null;
  }

  return (
    <div className="profile">
      <div className="profile-header">
        <h1>My Profile</h1>
      </div>

      <div className="profile-info">
        <h2>User Information</h2>
        <div className="info-item">
          <strong>Username:</strong> {user.username}
        </div>
        <div className="info-item">
          <strong>Email:</strong> {user.email || 'Not provided'}
        </div>
        <div className="info-item">
          <strong>Name:</strong>{' '}
          {user.first_name || user.last_name
            ? `${user.first_name || ''} ${user.last_name || ''}`.trim()
            : 'Not provided'}
        </div>
        <div className="info-item">
          <strong>Role:</strong> {user.is_staff ? 'Admin' : 'User'}
        </div>
      </div>

      <div className="profile-reviews">
        <h2>My Reviews ({reviews.length})</h2>
        {reviews.length === 0 ? (
          <p className="no-reviews">You haven't written any reviews yet.</p>
        ) : (
          <div className="reviews-list">
            {reviews.map((review) => (
              <div key={review.id} className="review-item">
                <div className="review-header">
                  <a href={`/movie/${review.movie}`} className="review-movie-link">
                    Movie #{review.movie}
                  </a>
                  <span className="review-rating">⭐ {review.rating}/10</span>
                </div>
                <p className="review-text">{review.text}</p>
                <span className="review-date">
                  {new Date(review.created_at).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;









