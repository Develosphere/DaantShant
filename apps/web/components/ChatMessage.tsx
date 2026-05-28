"use client";

import type { ChatMessage } from "@/lib/types";
import { DiagnosisReport } from "./DiagnosisReport";

type ChatMessageProps = {
  message: ChatMessage;
};

export function ChatMessageBubble({ message }: ChatMessageProps) {
  const isUser = message.sender === "user";
  
  return (
    <div className={`chat-message ${isUser ? "chat-message--user" : "chat-message--assistant"}`}>
      <div className="chat-message-header">
        <span className="chat-message-sender">
          {isUser ? "You" : "DantShaant AI"}
        </span>
        <span className="chat-message-time">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>
      
      <div className="chat-message-content">
        <p className="chat-message-text">{message.text}</p>
        
        {message.analysis_result && !isUser && (
          <div className="chat-message-analysis">
            <DiagnosisReport
              result={message.analysis_result}
              label="Analysis Results"
              loading={false}
              liveActive={false}
            />
          </div>
        )}
      </div>
    </div>
  );
}
