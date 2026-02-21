// src\theme\DocItem\Layout\index.tsx
import React, { useState, useCallback, useEffect, useContext } from 'react';
import DocItemLayout from '@theme-original/DocItem/Layout';
import TranslationControl, { clearSharedOriginalContent } from '../TranslationControl';
import Personalizer from '../Personalizer';
import type { Props } from '@theme/DocItem/Layout';
import styles from '../ContentControls.module.css';
import useIsBrowser from '@docusaurus/useIsBrowser';
import { useLocation } from '@docusaurus/router';
import { AuthContext } from '@site/src/components/AuthContext';

function AuthGate() {
  const { setShowAuthModal } = useContext(AuthContext);

  return (
    <div className={styles.authGate}>
      <div className={styles.authGateContent}>
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className={styles.authGateIcon}>
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
          <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
        <h2 className={styles.authGateTitle}>Sign in to access course content</h2>
        <p className={styles.authGateText}>
          Create a free account or sign in to access all modules, personalized learning, and AI-powered assistance.
        </p>
        <button
          className={styles.authGateButton}
          onClick={() => setShowAuthModal(true)}
        >
          Sign In to Continue
        </button>
      </div>
    </div>
  );
}

export default function DocItemLayoutWrapper(props: Props): JSX.Element {
  const { isAuthenticated, isLoading } = useContext(AuthContext);
  const [isTranslationActive, setIsTranslationActive] = useState(false);
  const [isPersonalizationActive, setIsPersonalizationActive] = useState(false);
  const isBrowser = useIsBrowser();
  const location = useLocation();

  // Reset states when navigating to a new page
  useEffect(() => {
    setIsTranslationActive(false);
    setIsPersonalizationActive(false);
    clearSharedOriginalContent();
  }, [location.pathname]);

  const handleTranslationStateChange = useCallback((isActive: boolean) => {
    setIsTranslationActive(isActive);
    if (isActive) {
      setIsPersonalizationActive(false);
    }
  }, []);

  const handlePersonalizationStateChange = useCallback((isActive: boolean) => {
    setIsPersonalizationActive(isActive);
    if (isActive) {
      setIsTranslationActive(false);
    }
  }, []);

  const resetTranslation = useCallback(() => {
    if (isBrowser && (window as any).__resetTranslation) {
      (window as any).__resetTranslation();
    }
    setIsTranslationActive(false);
  }, [isBrowser]);

  const resetPersonalization = useCallback(() => {
    if (isBrowser && (window as any).__resetPersonalization) {
      (window as any).__resetPersonalization();
    }
    setIsPersonalizationActive(false);
  }, [isBrowser]);

  // Show loading state while checking auth
  if (isLoading) {
    return <DocItemLayout {...props} />;
  }

  // Show auth gate if not authenticated
  if (!isAuthenticated) {
    return <AuthGate />;
  }

  return (
    <>
      <div className={styles.controlsBar}>
        <TranslationControl
          onStateChange={handleTranslationStateChange}
          otherTransformActive={isPersonalizationActive}
          onResetOther={resetPersonalization}
        />
        <Personalizer
          onStateChange={handlePersonalizationStateChange}
          otherTransformActive={isTranslationActive}
          onResetOther={resetTranslation}
        />
      </div>
      <DocItemLayout {...props} />
    </>
  );
}
