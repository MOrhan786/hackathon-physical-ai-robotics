import React from 'react';
import clsx from 'clsx';
import './Card.css';

const Card = ({
  children,
  className,
  variant = 'default',
  elevation = 'md',
  hoverable = false,
  ...props
}) => {
  const cardClasses = clsx(
    'pai-card',
    `pai-card--${variant}`,
    `pai-card--elevation-${elevation}`,
    {
      'pai-card--hoverable': hoverable,
    },
    className
  );

  return (
    <div className={cardClasses} {...props}>
      {children}
    </div>
  );
};

const CardHeader = ({ children, className, ...props }) => {
  const headerClasses = clsx('pai-card__header', className);
  return (
    <div className={headerClasses} {...props}>
      {children}
    </div>
  );
};

const CardBody = ({ children, className, ...props }) => {
  const bodyClasses = clsx('pai-card__body', className);
  return (
    <div className={bodyClasses} {...props}>
      {children}
    </div>
  );
};

const CardFooter = ({ children, className, ...props }) => {
  const footerClasses = clsx('pai-card__footer', className);
  return (
    <div className={footerClasses} {...props}>
      {children}
    </div>
  );
};

const CardMedia = ({ src, alt, className, ...props }) => {
  const mediaClasses = clsx('pai-card__media', className);
  return (
    <div className={mediaClasses} {...props}>
      <img src={src} alt={alt} />
    </div>
  );
};

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;
Card.Media = CardMedia;

export default Card;