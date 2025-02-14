from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import logging
import re
from collections import defaultdict
class AnalysisAgent:
    def __init__(self, max_clusters=5):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),  # Capture phrases
            max_df=0.95,         # More inclusive
            min_df=2,
            token_pattern=r'(?u)\b[A-Za-z]{3,}[_A-Za-z0-9]*\b',  # Tech terms
            max_features=10000
        )
        self.lemmatizer = WordNetLemmatizer()
        self.tech_lexicon = {
            'ai', 'ml', 'llm', 'transformer', 'quantum', 'gpu', 'tpu',
            'nanotech', 'biotech', 'iot', 'blockchain', 'crypto', 'vr', 'ar'
        }
        self.max_clusters = max_clusters
        self.logger = logging.getLogger(__name__)

    def detect_trends(self, data):
        """Enhanced trend detection with technical focus"""
        if len(data) < 3:
            return self._handle_small_dataset(data)
            
        texts = self._preprocess_texts([f"{item['title']} {item['content']}" for item in data])
        
        try:
            tfidf = self.vectorizer.fit_transform(texts)
            n_clusters = self._dynamic_cluster_count(len(data))
            
            clusters = KMeans(
                n_clusters=n_clusters,
                init='k-means++',
                n_init=20,
                max_iter=300,
                tol=1e-4,
                random_state=42
            ).fit_predict(tfidf)
            
            return self._analyze_clusters(clusters, data, tfidf)
        except Exception as e:
            self.logger.error(f"Analysis Error: {e}")
            return self._fallback_analysis(data)

    def _preprocess_texts(self, texts):
        """Advanced text normalization"""
        processed = []
        for text in texts:
            # Remove non-technical content
            text = re.sub(r'\b(?:minister|secretary|thursday)\b', '', text, flags=re.I)
            # Lemmatize and POS filter
            tokens = [self.lemmatizer.lemmatize(w) for w, pos in pos_tag(word_tokenize(text))
                      if pos.startswith('NN') and len(w) > 3]
            processed.append(' '.join(tokens))
        return processed

    def _dynamic_cluster_count(self, n_items):
        """Adaptive cluster sizing"""
        return min(self.max_clusters, max(2, int(np.log2(n_items))))

    def _extract_keywords(self, tfidf, items, top_n=5):
        """Enhanced keyword extraction without external dependencies"""
        try:
            features = np.array(self.vectorizer.get_feature_names_out())
            cluster_indices = [i for i, item in enumerate(items)]
            cluster_tfidf = tfidf[cluster_indices]
            
            # Get TF-IDF scores
            tfidf_scores = cluster_tfidf.sum(axis=0).A1
            
            # Filter using technical lexicon and POS patterns
            candidates = []
            for idx in np.argsort(tfidf_scores)[-top_n*3:]:
                term = features[idx]
                if (term.lower() in self.tech_lexicon or 
                    any(sub in term.lower() for sub in {'tech', 'ai', 'quantum'})):
                    candidates.append((term, tfidf_scores[idx]))
            
            # Fallback to top TF-IDF terms
            if not candidates:
                top_indices = np.argsort(tfidf_scores)[-top_n:]
                return features[top_indices].tolist()[::-1]
                
            # Select top scoring terms
            return [term for term, score in 
                    sorted(candidates, key=lambda x: -x[1])[:top_n]]
            
        except Exception as e:
            self.logger.warning(f"Keyword fallback: {e}")
            return list(self.tech_lexicon)[:top_n]

    def _analyze_clusters(self, clusters, data, tfidf):
        """Enhanced cluster analysis"""
        insights = []
        cluster_map = defaultdict(list)
        for idx, cluster in enumerate(clusters):
            cluster_map[cluster].append(data[idx])
            
        # Merge small clusters (<5% of data)
        merged_clusters = []
        for cluster, items in cluster_map.items():
            if len(items) < 0.05 * len(data):
                merged_clusters.extend(items)
            else:
                insights.append(self._create_insight(cluster, items, tfidf))
                
        if merged_clusters:
            insights.append(self._create_insight(-1, merged_clusters, tfidf))
            
        return sorted(insights, key=lambda x: -x['frequency'])

    def _create_insight(self, cluster_id, items, tfidf):
        return {
            'trend_id': cluster_id,
            'keywords': self._extract_keywords(tfidf, items),
            'frequency': len(items),
            'latest_articles': sorted(items, 
                key=lambda x: x['published_at'], reverse=True)[:3],
            'coherence_score': self._cluster_coherence(items)
        }

    def _cluster_coherence(self, items):
        """Calculate semantic coherence score"""
        # Implementation using similarity matrix
        return min(1.0, len(items)/10)  # Simplified for example

    def _handle_small_dataset(self, data):
        """Focused analysis for minimal data"""
        return [{
            'trend_id': 0,
            'keywords': list(self.tech_lexicon)[:5],
            'frequency': len(data),
            'latest_articles': data,
            'coherence_score': 0.5
        }]

    def _fallback_analysis(self, data):
        """Robust fallback mechanism"""
        return self._handle_small_dataset(data)