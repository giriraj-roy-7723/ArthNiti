import { MessageCircle } from 'lucide-react';
import EntrepreneurPage from './EntrepreneurPage';

export default function Chatbot() {
  return <EntrepreneurPage icon={MessageCircle} eyebrow="Entrepreneur workspace" title="Chatbot" description="Ask questions about your business, finances, and available support." />;
}