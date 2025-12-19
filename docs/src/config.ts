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
    apiUrl: customFields?.apiUrl || 'https://hackathon-physical-ai-robotics-production.up.railway.app/api',
    apiKey: customFields?.apiKey || '',
  };
}

// For use outside React components (fallback values)
export const API_URL = 'https://hackathon-physical-ai-robotics-production.up.railway.app';
export const API_KEY = '';
