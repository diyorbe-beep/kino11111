/**
 * Movie detail page with reviews
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { moviesAPI, reviewsAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { MEDIA_URL } from '../services/api';
import './MovieDetail.css';

const MovieDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [movie, setMovie] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reviewForm, setReviewForm] = useState({ rating: 5, text: '' });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMovie();
    loadReviews();
  }, [id]);

  const loadMovie = async () => {
    try {
      const response = await moviesAPI.get(id);
      setMovie(response.data);
    } catch (error) {
      console.error('Failed to load movie:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadReviews = async () => {
    try {
      const response = await reviewsAPI.list({ movie: id });
      setReviews(response.data);
    } catch (error) {
      console.error('Failed to load reviews:', error);
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login');
      return;
    }

    setError('');
    setSubmitting(true);

    try {
      await reviewsAPI.create({
        movie: parseInt(id),
        rating: parseInt(reviewForm.rating),
        text: reviewForm.text,
      });
      setReviewForm({ rating: 5, text: '' });
      loadReviews();
      loadMovie(); // Reload to update average rating
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          error.response?.data?.non_field_errors?.[0] ||
          'Failed to submit review'
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading movie...</div>;
  }

  if (!movie) {
    return <div className="error">Movie not found</div>;
  }

  const posterUrl = movie.poster
    ? `${MEDIA_URL}/${movie.poster}`
    : 'https://via.placeholder.com/400x600?text=No+Poster';

  return (
    <div className="movie-detail">
      <div className="movie-detail-header">
        <div className="movie-detail-poster">
          <img src={posterUrl} alt={movie.title} />
        </div>
        <div className="movie-detail-info">
          <h1>{movie.title}</h1>
          <div className="movie-meta">
            <span className="movie-year">{movie.release_year}</span>
            {movie.average_rating && (
              <span className="movie-rating">⭐ {movie.average_rating}/10</span>
            )}
          </div>
          {movie.genres && movie.genres.length > 0 && (
            <div className="movie-genres">
              {movie.genres.map((genre) => (
                <span key={genre.id} className="genre-tag">
                  {genre.name}
                </span>
              ))}
            </div>
          )}
          {movie.actors && movie.actors.length > 0 && (
            <div className="movie-actors">
              <strong>Cast:</strong>{' '}
              {movie.actors.map((actor) => actor.name).join(', ')}
            </div>
          )}
          <div className="movie-description">
            <h3>Description</h3>
            <p>{movie.description}</p>
          </div>
        </div>
      </div>

      <div className="movie-reviews">
        <h2>Reviews ({reviews.length})</h2>

        {user && (
          <form onSubmit={handleReviewSubmit} className="review-form">
            <h3>Write a Review</h3>
            {error && <div className="form-error">{error}</div>}
            <div className="form-group">
              <label htmlFor="rating">Rating (1-10)</label>
              <input
                type="number"
                id="rating"
                min="1"
                max="10"
                value={reviewForm.rating}
                onChange={(e) =>
                  setReviewForm({ ...reviewForm, rating: e.target.value })
                }
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="text">Review Text</label>
              <textarea
                id="text"
                rows="4"
                value={reviewForm.text}
                onChange={(e) =>
                  setReviewForm({ ...reviewForm, text: e.target.value })
                }
                required
              />
            </div>
            <button type="submit" disabled={submitting} className="form-button">
              {submitting ? 'Submitting...' : 'Submit Review'}
            </button>
          </form>
        )}

        <div className="reviews-list">
          {reviews.length === 0 ? (
            <p className="no-reviews">No reviews yet. Be the first to review!</p>
          ) : (
            reviews.map((review) => (
              <div key={review.id} className="review-item">
                <div className="review-header">
                  <strong>{review.user}</strong>
                  <span className="review-rating">⭐ {review.rating}/10</span>
                </div>
                <p className="review-text">{review.text}</p>
                <span className="review-date">
                  {new Date(review.created_at).toLocaleDateString()}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;








