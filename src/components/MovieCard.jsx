/**
 * Movie card component for displaying movie information
 */
import { Link } from 'react-router-dom';
import { MEDIA_URL } from '../services/api';
import './MovieCard.css';

const MovieCard = ({ movie }) => {
  const posterUrl = movie.poster
    ? `${MEDIA_URL}/${movie.poster}`
    : 'https://via.placeholder.com/300x450?text=No+Poster';

  return (
    <Link to={`/movie/${movie.id}`} className="movie-card">
      <div className="movie-card-poster">
        <img src={posterUrl} alt={movie.title} />
        {movie.average_rating && (
          <div className="movie-card-rating">
            ⭐ {movie.average_rating}
          </div>
        )}
      </div>
      <div className="movie-card-info">
        <h3 className="movie-card-title">{movie.title}</h3>
        <p className="movie-card-year">{movie.release_year}</p>
        {movie.genres && movie.genres.length > 0 && (
          <div className="movie-card-genres">
            {movie.genres.slice(0, 2).map((genre) => (
              <span key={genre.id} className="genre-tag">
                {genre.name}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
};

export default MovieCard;









