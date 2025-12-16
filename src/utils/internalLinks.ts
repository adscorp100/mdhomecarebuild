/**
 * Internal Linking Utility
 * Provides functions for generating related content links to improve
 * internal link structure and SEO authority flow.
 */

import type { CollectionEntry } from 'astro:content';

// Suburb data with regions for nearby suburb calculation
interface SuburbInfo {
  state: string;
  region: string;
}

interface SuburbData {
  [key: string]: SuburbInfo;
}

/**
 * Get nearby suburbs in the same region
 * Returns suburbs from the same region, excluding the current suburb
 */
export function getNearbySuburbs(
  currentSuburbSlug: string,
  currentRegion: string,
  suburbsData: SuburbData,
  limit: number = 6
): Array<{ slug: string; name: string; region: string }> {
  const nearbySuburbs: Array<{ slug: string; name: string; region: string }> = [];

  for (const [slug, info] of Object.entries(suburbsData)) {
    if (slug !== currentSuburbSlug && info.region === currentRegion) {
      nearbySuburbs.push({
        slug,
        name: formatSuburbName(slug),
        region: info.region
      });
    }
  }

  // Shuffle and limit results for variety
  return shuffleArray(nearbySuburbs).slice(0, limit);
}

/**
 * Get related services in the same category
 */
export function getRelatedServices(
  currentService: CollectionEntry<'services'>,
  allServices: CollectionEntry<'services'>[],
  limit: number = 3
): CollectionEntry<'services'>[] {
  return allServices
    .filter(
      (service) =>
        service.data.category === currentService.data.category &&
        service.slug !== currentService.slug
    )
    .slice(0, limit);
}

/**
 * Get related blog posts based on service keywords
 */
export function getRelatedBlogPosts(
  serviceKeywords: string[],
  allBlogPosts: CollectionEntry<'blog'>[],
  limit: number = 3
): CollectionEntry<'blog'>[] {
  if (!serviceKeywords || serviceKeywords.length === 0) {
    // Return most recent posts if no keywords
    return allBlogPosts
      .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf())
      .slice(0, limit);
  }

  // Clean keywords (remove {suburb} placeholders)
  const cleanedKeywords = serviceKeywords
    .map((k) => k.replace(/{suburb}/g, '').trim().toLowerCase())
    .filter((k) => k.length > 2);

  // Score posts by keyword relevance
  const scoredPosts = allBlogPosts.map((post) => {
    const titleLower = post.data.title.toLowerCase();
    const descLower = post.data.description.toLowerCase();
    const tagsLower = (post.data.tags || []).map((t: string) => t.toLowerCase());

    let score = 0;
    for (const keyword of cleanedKeywords) {
      if (titleLower.includes(keyword)) score += 3;
      if (descLower.includes(keyword)) score += 2;
      if (tagsLower.some((tag: string) => tag.includes(keyword))) score += 2;
    }

    return { post, score };
  });

  // Return top scoring posts
  return scoredPosts
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((item) => item.post);
}

/**
 * Get services available in a specific suburb
 * Useful for "Other services in [suburb]" sections
 */
export function getServicesInSuburb(
  allServices: CollectionEntry<'services'>[],
  currentServiceSlug: string,
  limit: number = 6
): CollectionEntry<'services'>[] {
  return allServices
    .filter((service) => service.slug !== currentServiceSlug)
    .sort(() => Math.random() - 0.5) // Randomize for variety
    .slice(0, limit);
}

/**
 * Get suburbs where a service is available, grouped by state
 */
export function getSuburbsByState(
  suburbsData: SuburbData
): Record<string, Array<{ slug: string; name: string; region: string }>> {
  const byState: Record<string, Array<{ slug: string; name: string; region: string }>> = {};

  for (const [slug, info] of Object.entries(suburbsData)) {
    if (!byState[info.state]) {
      byState[info.state] = [];
    }
    byState[info.state].push({
      slug,
      name: formatSuburbName(slug),
      region: info.region
    });
  }

  // Sort suburbs alphabetically within each state
  for (const state of Object.keys(byState)) {
    byState[state].sort((a, b) => a.name.localeCompare(b.name));
  }

  return byState;
}

/**
 * Format a suburb slug into a display name
 * e.g., "bondi-junction" -> "Bondi Junction"
 */
export function formatSuburbName(slug: string): string {
  return slug
    .split('-')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Get breadcrumb items for a service/suburb page
 */
export function getBreadcrumbs(
  serviceTitle: string,
  serviceSlug: string,
  suburbName?: string,
  suburbSlug?: string
): Array<{ name: string; url: string }> {
  const breadcrumbs = [
    { name: 'Home', url: 'https://mdhomecare.com.au' },
    { name: 'Services', url: 'https://mdhomecare.com.au/services' },
    {
      name: serviceTitle.replace(/{suburb}/g, 'Australia').split('|')[0].trim(),
      url: `https://mdhomecare.com.au/services/${serviceSlug}`
    }
  ];

  if (suburbName && suburbSlug) {
    breadcrumbs.push({
      name: suburbName,
      url: `https://mdhomecare.com.au/services/${serviceSlug}/${suburbSlug}`
    });
  }

  return breadcrumbs;
}

/**
 * Generate canonical URL for a page
 */
export function getCanonicalUrl(
  serviceSlug: string,
  suburbSlug?: string
): string {
  const baseUrl = 'https://mdhomecare.com.au';
  if (suburbSlug) {
    return `${baseUrl}/services/${serviceSlug}/${suburbSlug}`;
  }
  return `${baseUrl}/services/${serviceSlug}`;
}

/**
 * Fisher-Yates shuffle algorithm
 */
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Extract clean service name from title (without suburb placeholder)
 */
export function getCleanServiceName(title: string): string {
  return title
    .replace(/{suburb}/g, '')
    .replace(/\s+in\s*$/, '')
    .replace(/\s*\|.*$/, '')
    .trim();
}

/**
 * Generate schema-friendly service type based on category
 */
export function getServiceType(category: string): string {
  const typeMap: Record<string, string> = {
    'Home Support': 'HomeHealthCareService',
    'Personal Support': 'HealthAndBeautyBusiness',
    'Daily Living Support': 'HomeHealthCareService',
    'Caregiver Support': 'HomeHealthCareService',
    'Disability Services': 'HomeHealthCareService',
    'Support Coordination': 'ProfessionalService',
    'Clinical Services': 'MedicalBusiness',
    'Allied Health': 'MedicalBusiness',
    'Therapy Services': 'MedicalBusiness',
    'Accommodation': 'LodgingBusiness',
    'Transport': 'TaxiService'
  };

  return typeMap[category] || 'HomeHealthCareService';
}
