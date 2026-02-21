// src\config.ts
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// For use in React components
export function useApiConfig() {
  const { siteConfig } = useDocusaurusContext();
  const customFields = siteConfig.customFields as {
    apiUrl?: string;
    apiKey?: string;
  };
  
  return {
    apiUrl: customFields?.apiUrl || 'https://mrsasif-hackathon1-c.hf.space',
    apiKey: customFields?.apiKey || 'password123',
  };
}

// For use outside React components (fallback values)
export const API_URL = 'https://mrsasif-hackathon1-c.hf.space';
export const API_KEY = 'password123';
