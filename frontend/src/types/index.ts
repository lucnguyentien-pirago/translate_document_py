export interface DocumentContent {
  content: string;
  translated_content?: string;
}

export interface TranslationViewProps {
  content: DocumentContent[];
  translatedContent: DocumentContent[] | null;
}

export interface TranslationViewEmits {
  (e: 'update:translatedContent', value: DocumentContent[]): void;
} 