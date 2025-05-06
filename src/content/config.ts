import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
  }),
});

const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    category: z.string(),
    image: z.string().optional(),
    keywords: z.array(z.string()).default([]),
  }),
});

// Define schema for providers collection
const providersCollection = defineCollection({
  schema: z.object({
    name: z.string(),
    description: z.string(),
    category: z.string(),
    phone: z.string().optional(),
    email: z.string().optional(),
    website: z.string().optional(),
    address: z.string().optional(),
    services: z.array(z.string()).optional(),
    operatingHours: z.string().optional(),
    ndisRegistered: z.boolean().optional(),
    agedCareRegistered: z.boolean().optional(),
    claimed: z.boolean().default(false),
  }),
});

const jobsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.string(),
    requirements: z.array(z.string()),
    certifications: z.array(z.string()),
    image: z.string().optional(),
    metaTitle: z.string(),
    metaDescription: z.string(),
    canonicalUrl: z.string().optional(),
    noindex: z.boolean().optional(),
    featured: z.boolean().optional(),
  }),
});

export const collections = {
  'blog': blog,
  'services': services,
  'providers': providersCollection,
  'jobs': jobsCollection,
}; 