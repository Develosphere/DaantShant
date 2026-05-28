"""LLM-powered conversational engine for DaantShaant assistant."""

import logging
from typing import Optional
from datetime import datetime

from orchestrator.chat_schemas import AnalysisHistoryDocument, MessageDocument
from orchestrator.openrouter_client import openrouter_client

logger = logging.getLogger(__name__)


ASSISTANT_SYSTEM_PROMPT = """You are DaantShaant, a caring and knowledgeable oral health assistant.

Your role:
- Help users understand their oral health
- Provide evidence-based dental care guidance
- Analyze teeth images when provided
- Answer questions about brushing, flossing, dental conditions, and oral hygiene
- Encourage good dental habits

Your personality:
- Conversational and friendly, but professional
- Caring without being overly emotional
- Clear and educational
- Ask relevant follow-up questions naturally
- Reference previous context when useful

Important boundaries:
- You are an AWARENESS TOOL, not a medical diagnosis system
- Never claim diagnostic certainty
- Always recommend consulting a licensed dentist for professional evaluation
- Do not provide treatment plans or prescribe medications
- Stay focused on oral health topics
- Politely redirect off-topic conversations

Communication style:
- Use simple, clear language
- Break complex topics into digestible points
- Provide actionable advice when appropriate
- Be encouraging about improvements
- Show empathy for concerns or symptoms

Always end responses about potential issues with: "For a professional evaluation, please consult your dentist."
"""


class ConversationEngine:
    """LLM-powered conversation engine using OpenRouter."""
    
    def __init__(self):
        self.client = openrouter_client
    
    def _build_context(
        self,
        recent_messages: list[MessageDocument],
        previous_analyses: Optional[list[AnalysisHistoryDocument]] = None
    ) -> str:
        """Build context string from conversation history."""
        context_parts = []
        
        # Add recent conversation
        if recent_messages:
            context_parts.append("Recent conversation:")
            for msg in recent_messages[-5:]:  # Last 5 messages
                sender = "User" if msg.sender == "user" else "You"
                # Truncate long messages
                text = msg.text[:200] + "..." if len(msg.text) > 200 else msg.text
                context_parts.append(f"{sender}: {text}")
        
        # Add previous analysis summary
        if previous_analyses:
            context_parts.append("\nPrevious analysis history:")
            for analysis in previous_analyses[:3]:  # Last 3 analyses
                date = analysis.created_at.strftime("%B %d")
                context_parts.append(
                    f"- {date}: {analysis.condition_label} (severity: {analysis.severity})"
                )
        
        return "\n".join(context_parts) if context_parts else "No previous context."
    
    def _build_conversation_context(
        self,
        recent_messages: list[MessageDocument]
    ) -> list[dict]:
        """Build conversation context for OpenRouter API."""
        context = []
        for msg in recent_messages[-6:]:  # Last 6 messages (3 exchanges)
            role = "user" if msg.sender == "user" else "assistant"
            # Truncate very long messages
            content = msg.text[:500] + "..." if len(msg.text) > 500 else msg.text
            context.append({"role": role, "content": content})
        return context
    
    async def generate_greeting(self) -> str:
        """Generate greeting response."""
        logger.info("[LLM] Generating greeting")
        try:
            prompt = "The user greeted you. Respond warmly and briefly introduce what you can help with. Keep it conversational and inviting. Mention you can analyze teeth photos and answer oral health questions."
            
            response = await self.client.generate_chat_response(
                system_prompt=ASSISTANT_SYSTEM_PROMPT,
                user_message=prompt,
                temperature=0.7,
                max_tokens=200
            )
            logger.info("[LLM] Greeting generated successfully")
            return response
        except Exception as e:
            logger.error(f"[LLM] Greeting generation failed: {e}")
            return (
                "Hello! I'm DaantShaant, your oral health assistant. "
                "I can help answer questions about dental care and analyze photos of your teeth. "
                "How can I help you today?"
            )
    
    async def generate_general_response(
        self,
        user_message: str,
        recent_messages: list[MessageDocument],
        previous_analyses: Optional[list[AnalysisHistoryDocument]] = None
    ) -> str:
        """Generate response to general oral health question."""
        logger.info("[LLM] Generating general response")
        context_str = self._build_context(recent_messages, previous_analyses)
        conversation_context = self._build_conversation_context(recent_messages)
        
        prompt = f"""The user asked an oral health question. Provide a helpful, evidence-based answer.
Be conversational and educational. If relevant, ask a follow-up question to better understand their situation.

User's question: {user_message}

Context: {context_str}"""
        
        try:
            response = await self.client.generate_chat_response(
                system_prompt=ASSISTANT_SYSTEM_PROMPT,
                user_message=prompt,
                conversation_context=conversation_context,
                temperature=0.7,
                max_tokens=500
            )
            logger.info("[LLM] General response generated successfully")
            return response
        except Exception as e:
            logger.error(f"[LLM] General response generation failed: {e}")
            return (
                "I'm here to help with your oral health questions. "
                "Could you provide more details about what you'd like to know? "
                "I can discuss brushing techniques, dental conditions, or analyze photos of your teeth."
            )
    
    async def generate_symptom_response(
        self,
        user_message: str,
        recent_messages: list[MessageDocument],
        previous_analyses: Optional[list[AnalysisHistoryDocument]] = None
    ) -> str:
        """Generate response to symptom discussion."""
        logger.info("[LLM] Generating symptom response")
        context_str = self._build_context(recent_messages, previous_analyses)
        conversation_context = self._build_conversation_context(recent_messages)
        
        prompt = f"""The user is describing symptoms or concerns about their oral health.
Acknowledge their concern with empathy. Provide general guidance about what might cause such symptoms.
Recommend seeing a dentist for proper evaluation. Ask clarifying questions if helpful.

User's message: {user_message}

Context: {context_str}"""
        
        try:
            response = await self.client.generate_chat_response(
                system_prompt=ASSISTANT_SYSTEM_PROMPT,
                user_message=prompt,
                conversation_context=conversation_context,
                temperature=0.7,
                max_tokens=500
            )
            logger.info("[LLM] Symptom response generated successfully")
            return response
        except Exception as e:
            logger.error(f"[LLM] Symptom response generation failed: {e}")
            return (
                "I understand you're experiencing some discomfort. "
                "While I can provide general information, symptoms like these should be evaluated by a dentist. "
                "They can properly diagnose the issue and recommend appropriate treatment. "
                "In the meantime, maintain gentle oral hygiene and avoid irritating the affected area."
            )
    
    async def generate_analysis_response(
        self,
        user_message: str,
        analysis_result: dict,
        recent_messages: list[MessageDocument],
        previous_analyses: Optional[list[AnalysisHistoryDocument]] = None
    ) -> str:
        """Generate conversational response for image analysis."""
        logger.info("[LLM] Generating analysis response")
        diagnosis = analysis_result.get("diagnosis", {})
        condition = diagnosis.get("condition_label", "Unknown")
        severity = diagnosis.get("severity", "unknown")
        confidence = diagnosis.get("confidence", 0.0)
        findings = analysis_result.get("analysis", {}).get("findings", [])
        
        findings_text = ", ".join([f["label"] for f in findings]) if findings else "none"
        context_str = self._build_context(recent_messages, previous_analyses)
        conversation_context = self._build_conversation_context(recent_messages)
        
        prompt = f"""The user shared a teeth image for analysis. You've analyzed it and found:

Condition: {condition}
Severity: {severity}
Confidence: {confidence:.0%}
Findings: {findings_text}

Provide a conversational explanation of what you observed. Be clear but not alarming.
Explain what the findings mean in simple terms. Provide actionable advice for improvement.
If severity is concerning, recommend dental consultation.

User's message: {user_message or "Please analyze this image"}

Context: {context_str}"""
        
        try:
            response = await self.client.generate_chat_response(
                system_prompt=ASSISTANT_SYSTEM_PROMPT,
                user_message=prompt,
                conversation_context=conversation_context,
                temperature=0.7,
                max_tokens=600
            )
            
            # Ensure disclaimer is present
            if "awareness tool" not in response.lower() and "not a medical diagnosis" not in response.lower():
                response += (
                    "\n\n*Please note: This is an awareness tool, not a medical diagnosis. "
                    "Always consult a licensed dentist for professional evaluation.*"
                )
            
            logger.info("[LLM] Analysis response generated successfully")
            return response
        except Exception as e:
            logger.error(f"[LLM] Analysis response generation failed: {e}")
            return self._fallback_analysis_response(condition, severity, findings_text)
    
    async def generate_follow_up_response(
        self,
        user_message: str,
        recent_messages: list[MessageDocument]
    ) -> str:
        """Generate response to follow-up message."""
        logger.info("[LLM] Generating follow-up response")
        context_str = self._build_context(recent_messages)
        conversation_context = self._build_conversation_context(recent_messages)
        
        prompt = f"""The user sent a brief follow-up message. Consider the conversation context and respond naturally.

User's message: {user_message}

Recent conversation: {context_str}"""
        
        try:
            response = await self.client.generate_chat_response(
                system_prompt=ASSISTANT_SYSTEM_PROMPT,
                user_message=prompt,
                conversation_context=conversation_context,
                temperature=0.7,
                max_tokens=300
            )
            logger.info("[LLM] Follow-up response generated successfully")
            return response
        except Exception as e:
            logger.error(f"[LLM] Follow-up response generation failed: {e}")
            return "I'm here to help. What else would you like to know about your oral health?"
    
    async def generate_comparison_response(
        self,
        user_message: str,
        current_analysis: Optional[dict],
        previous_analyses: list[AnalysisHistoryDocument]
    ) -> str:
        """Generate response comparing current and previous analyses."""
        logger.info("[LLM] Generating comparison response")
        if not previous_analyses:
            return (
                "I don't have any previous analysis to compare with yet. "
                "Share another photo in the future, and I'll be able to track your progress!"
            )
        
        current_findings = "No current analysis"
        if current_analysis:
            diagnosis = current_analysis.get("diagnosis", {})
            current_findings = f"{diagnosis.get('condition_label', 'Unknown')} (severity: {diagnosis.get('severity', 'unknown')})"
        
        previous_findings = []
        for analysis in previous_analyses[:3]:
            date = analysis.created_at.strftime("%B %d")
            previous_findings.append(f"{date}: {analysis.condition_label} (severity: {analysis.severity})")
        
        prompt = f"""The user wants to compare with previous analysis or track progress.

Current findings: {current_findings}
Previous analysis:
{chr(10).join(previous_findings)}

Provide a comparison and note any improvements or concerns. Be encouraging about positive changes.

User's message: {user_message}"""
        
        try:
            response = await self.client.generate_chat_response(
                system_prompt=ASSISTANT_SYSTEM_PROMPT,
                user_message=prompt,
                temperature=0.7,
                max_tokens=400
            )
            logger.info("[LLM] Comparison response generated successfully")
            return response
        except Exception as e:
            logger.error(f"[LLM] Comparison response generation failed: {e}")
            return "I can see your previous scans. Keep up with regular dental care and consistent oral hygiene!"
    
    def _fallback_analysis_response(self, condition: str, severity: str, findings: str) -> str:
        """Fallback template-based response if LLM fails."""
        response_parts = ["I've analyzed your teeth image."]
        
        if condition == "Healthy":
            response_parts.append(
                "Good news! Your teeth appear healthy overall. "
                "Keep up with your regular brushing and flossing routine."
            )
        elif "cavity" in condition.lower():
            response_parts.append(
                "I detected signs of tooth decay. "
                "I recommend scheduling a dental appointment for proper evaluation and treatment."
            )
        elif "plaque" in condition.lower() or "tartar" in condition.lower():
            response_parts.append(
                "I noticed some plaque buildup. "
                "Consistent brushing and flossing can help improve this."
            )
        elif "gum" in condition.lower() or "gingivitis" in condition.lower():
            response_parts.append(
                "I see signs of gum inflammation. "
                "Focus on gentle brushing along the gum line and daily flossing."
            )
        else:
            response_parts.append(
                "I had difficulty analyzing this image clearly. "
                "Try taking a photo in better lighting with teeth clearly visible."
            )
        
        response_parts.append(
            "\n\n*Please note: This is an awareness tool, not a medical diagnosis. "
            "Always consult a licensed dentist for professional evaluation.*"
        )
        
        return " ".join(response_parts)


# Global conversation engine instance
conversation_engine = ConversationEngine()
