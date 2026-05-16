"""ChromaDB client for memory management."""
import chromadb
import os
from typing import List, Dict, Optional
from datetime import datetime
import streamlit as st


class ChromaMemoryClient:
    """Client for ChromaDB memory management."""
    
    def __init__(self, collection_name: str = "voice_assistant_memory"):
        """
        Initialize ChromaDB client.
        
        Args:
            collection_name: Name of the ChromaDB collection
        """
        # Initialize persistent ChromaDB client
        chroma_dir = os.path.join(os.path.expanduser("~"), ".voice_assistant", "chroma_data")
        os.makedirs(chroma_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=chroma_dir)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_to_memory(
        self,
        text: str,
        response: str,
        user_id: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Add interaction to memory.
        
        Args:
            text: User input text
            response: AI response text
            user_id: User identifier
            metadata: Additional metadata
        """
        try:
            doc_id = f"{user_id}_{datetime.now().timestamp()}"
            
            combined_text = f"User: {text}\nAssistant: {response}"
            
            meta = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "input_length": len(text),
                "response_length": len(response)
            }
            
            if metadata:
                meta.update(metadata)
            
            self.collection.add(
                ids=[doc_id],
                documents=[combined_text],
                metadatas=[meta]
            )
        
        except Exception as e:
            st.warning(f"Error adding to memory: {str(e)}")
    
    def search(
        self,
        query: str,
        k: int = 3,
        user_id: Optional[str] = None
    ) -> List[str]:
        """
        Search memory for similar interactions.
        
        Args:
            query: Search query
            k: Number of results to return
            user_id: Filter by user ID
            
        Returns:
            List of relevant memories
        """
        try:
            # Build where filter if user_id provided
            where_filter = None
            if user_id:
                where_filter = {"user_id": {"$eq": user_id}}
            
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=where_filter
            )
            
            # Extract documents
            if results["documents"] and len(results["documents"]) > 0:
                return results["documents"][0]
            
            return []
        
        except Exception as e:
            st.warning(f"Error searching memory: {str(e)}")
            return []
    
    def get_all_memories(self, user_id: Optional[str] = None) -> List[Dict]:
        """
        Get all memories for a user.
        
        Args:
            user_id: Filter by user ID
            
        Returns:
            List of memory items
        """
        try:
            # Build where filter if user_id provided
            where_filter = None
            if user_id:
                where_filter = {"user_id": {"$eq": user_id}}
            
            results = self.collection.get(where=where_filter)
            
            memories = []
            for i, doc in enumerate(results.get("documents", [])):
                memories.append({
                    "id": results["ids"][i],
                    "text": doc,
                    "metadata": results["metadatas"][i] if results.get("metadatas") else {}
                })
            
            return memories
        
        except Exception as e:
            st.warning(f"Error getting memories: {str(e)}")
            return []
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a specific memory.
        
        Args:
            memory_id: Memory identifier
            
        Returns:
            True if successful
        """
        try:
            self.collection.delete(ids=[memory_id])
            return True
        except Exception as e:
            st.warning(f"Error deleting memory: {str(e)}")
            return False
    
    def clear_user_memories(self, user_id: str) -> bool:
        """
        Clear all memories for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        try:
            where_filter = {"user_id": {"$eq": user_id}}
            
            results = self.collection.get(where=where_filter)
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
            
            return True
        except Exception as e:
            st.warning(f"Error clearing user memories: {str(e)}")
            return False
    
    def get_memory_stats(self, user_id: Optional[str] = None) -> Dict:
        """
        Get memory statistics.
        
        Args:
            user_id: Filter by user ID
            
        Returns:
            Statistics dictionary
        """
        try:
            memories = self.get_all_memories(user_id)
            
            total_chars = sum(len(m["text"]) for m in memories)
            
            stats = {
                "total_memories": len(memories),
                "total_characters": total_chars,
                "avg_length": total_chars // len(memories) if memories else 0
            }
            
            return stats
        
        except Exception as e:
            st.warning(f"Error getting stats: {str(e)}")
            return {}
    
    def rebuild_index(self) -> None:
        """Rebuild the ChromaDB index."""
        try:
            # Get all data
            all_data = self.collection.get()
            
            # Delete and recreate collection
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            # Re-add all data
            if all_data["documents"]:
                self.collection.add(
                    ids=all_data["ids"],
                    documents=all_data["documents"],
                    metadatas=all_data["metadatas"]
                )
        
        except Exception as e:
            st.warning(f"Error rebuilding index: {str(e)}")
