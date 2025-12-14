import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './HomepageHero.css';

export default function HomepageHero() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <header className={clsx('hero hero--primary', 'pai-hero')}>
      <div className="container">
        <div className="pai-hero-content">
          <div className="pai-hero-visual-elements">
            <div className="pai-shape pai-shape-1"></div>
            <div className="pai-shape pai-shape-2"></div>
            <div className="pai-shape pai-shape-3"></div>
          </div>
          <div className="pai-hero-text-content">
            <div className="pai-badge">Open Source Textbook</div>
            <h1 className="pai-hero-title">
              {siteConfig.title}
            </h1>
            <p className="pai-hero-subtitle">
              {siteConfig.tagline}
            </p>
            <div className="pai-hero-buttons">
              <Link
                className="button button--secondary button--lg pai-button pai-button-primary"
                to="/docs/intro">
                Get Started
              </Link>
              <Link
                className="button button--outline button--lg pai-button pai-button-secondary"
                to="/docs/tutorial">
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}