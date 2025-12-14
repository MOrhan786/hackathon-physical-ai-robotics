import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import './Button.css';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  disabled = false,
  href,
  onClick,
  className,
  type = 'button',
  ...props
}) => {
  const buttonClasses = clsx(
    'pai-button',
    `pai-button--${variant}`,
    `pai-button--${size}`,
    {
      'pai-button--full-width': fullWidth,
      'pai-button--disabled': disabled,
    },
    className
  );

  // Determine if it should be a Link or a button element
  if (href) {
    return (
      <Link
        to={href}
        className={buttonClasses}
        onClick={disabled ? (e) => e.preventDefault() : onClick}
        {...props}
      >
        {children}
      </Link>
    );
  }

  return (
    <button
      type={type}
      className={buttonClasses}
      onClick={disabled ? undefined : onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;