import React, { useEffect, useState,useRef } from 'react';
import { 
  Plus, 
  ExternalLink, 
  PanelLeftClose, 
  MessageSquare, 
  Send 
} from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
export default function App() {
  const [messages, setMessages] = useState([]);
  const [inputVal, setInputVal] = useState('');
  const [isResponding,setResponding] = useState(false)
  const [recentChats,setChats] = useState(()=>{
    const chats = localStorage.getItem("recentChats")

    if(chats){
      return JSON.parse(chats)
    }
    return []
  })
  const [currentChat,setCurrentChat] = useState(0)

const currentChatRef = useRef(currentChat)
useEffect(() => { currentChatRef.current = currentChat }, [currentChat])


  useEffect(()=>{
    localStorage.setItem("recentChats",JSON.stringify(recentChats))
  },[recentChats])

  useEffect(()=>{
    setMessages(
recentChats.find((chat)=>chat.id==currentChat)?.messages || []
    )
  },[currentChat])

  const get_response = async (query) => {
    setResponding(true)
    const url = `${import.meta.env.VITE_API_URL}/ask`
    const chatId = currentChat
    try {
      const queryData = { query: query }
      const response = await axios.post(url, queryData)
      const newMsg = { role: 'llm', content: response.data.answer }
  
      setChats((prev) =>
        prev.map((chat) =>
          chatId === chat.id ? { ...chat, messages: [...chat.messages, newMsg] } : chat
        )
      )
  
      if (currentChatRef.current === chatId) {
        setMessages((prev) => [...prev, newMsg])
      }
    } catch (error) {
      console.error(error)
    } finally {
      setResponding(false)
    }
  }

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputVal.trim()) return;

    setMessages((prev) => [...prev, { role: 'user', content: inputVal }]);
    if(messages.length == 0) setChats((prev)=>[...prev,{id:recentChats.length,
      title:inputVal.slice(0,35),messages:[{ role: 'user', content:inputVal}]}])
    get_response(inputVal)
    setInputVal('');
  };
  useEffect(()=>{
    setChats((prev)=> prev.map((chat,_)=>{
      if(chat.id == currentChat) {
        return {...chat,messages}
      }
      return chat
    }))
  },[messages])
  return (
    <div className="flex flex-col h-screen w-full bg-slate-50 font-sans text-slate-800 overflow-hidden">
      

      <nav className="h-16 w-full bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0 z-10">
        <div className="flex items-center gap-2">
          <span className="text-xl font-bold tracking-tight text-slate-900">
            PyTorch RAG 
          </span>
        </div>
        
        <a 
          href="https://pytorch.org/docs/stable/index.html" 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
        >
          PyTorch Docs <ExternalLink className="w-4 h-4" />
        </a>
      </nav>

      <div className="flex flex-1 w-full overflow-hidden">
        

        <aside className="w-[320px] bg-zinc-900 text-zinc-100 flex flex-col p-4 shrink-0 border-r border-zinc-800">

          <div className="flex items-center gap-2 mb-4">
            <button 
              type="button" 
              className="p-2.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 transition-colors border border-zinc-700/50"
              title="Collapse sidebar"
              onClick={()=>alert("Dev will work on this button!!!")}
            >
              <PanelLeftClose className="w-5 h-5" />
            </button>

           
            <button 
              type="button"
              onClick={() => {
                setCurrentChat(recentChats.length)
              }}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg shadow-sm transition-all active:scale-[0.98]"
            >
              <Plus className="w-5 h-5" />
              <span>New Chat</span>
            </button>
          </div>
          <div className="flex-1 overflow-y-auto no-scrollbar">
            <h3 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-3 px-2">
              Recent Chats
            </h3>
            <div className="flex flex-col gap-1">
              {recentChats.map((chat, idx) => (
                <button 
                  key={idx}
                  onClick={()=>
                    setCurrentChat(chat.id)}
                  className="flex items-center gap-3 px-3 py-2.5 text-sm text-zinc-300 rounded-lg hover:bg-zinc-800 hover:text-white transition-colors text-left truncate"
                >
                  <MessageSquare className="w-4 h-4 shrink-0 opacity-60" />
                  <span className="truncate">{chat.title}</span>
                </button>
              ))}
            </div>
          </div>
        </aside>
                    {console.log(currentChat)}
        <main className="flex-1 flex flex-col h-full bg-slate-50 relative overflow-hidden">
          
        
          <div 
            tabIndex={0}
            className="flex-1 overflow-y-auto p-4 md:p-8 outline-none [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]"
          >
            <div className="max-w-3xl mx-auto h-full flex flex-col">
              
          
              {messages.length === 0 ? (
                <div className="my-auto flex flex-col items-center justify-center text-center p-8 rounded-2xl bg-white border border-slate-200 shadow-sm">
                  <h1 className="text-3xl font-bold text-slate-900 mb-2">
                    PyTorch RAG
                  </h1>
                  <p className="text-base text-slate-500">
                    Ask questions about the PyTorch docs.
                  </p>
                </div>
              ) : (
                /* Chat Messages Stream */
                <div className="flex flex-col gap-4 py-4">
                  {messages.map((msg, index) => (
                    <div 
                      key={index} 
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[80%] rounded-xl px-4 py-3 text-sm shadow-sm ${
                        msg.role === 'user' 
                          ? 'bg-blue-600 text-white rounded-br-none' 
                          : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none'
                      }`}>
            <ReactMarkdown
  remarkPlugins={[remarkGfm,remarkBreaks]}
  components={{
    h1: ({ children }) => (
      <h1 className="text-2xl font-bold mt-4 mb-3">
        {children}
      </h1>
    ),

    h2: ({ children }) => (
      <h2 className="text-xl font-bold mt-4 mb-3">
        {children}
      </h2>
    ),

    h3: ({ children }) => (
      <h3 className="text-lg font-semibold mt-4 mb-2">
        {children}
      </h3>
    ),

    p: ({ children }) => (
      <p className="mb-4 leading-7">
        {children}
      </p>
    ),

    ul: ({ children }) => (
      <ul className="list-disc ml-5 mb-4 space-y-1">
        {children}
      </ul>
    ),

    ol: ({ children }) => (
      <ol className="list-decimal ml-5 mb-4 space-y-1">
        {children}
      </ol>
    ),

    // Inline code: torch.add(), abs_(), etc.
    code: ({ children, className }) => {
      const isBlock = className?.includes("language-");

      if (isBlock) {
        return (
          <code className="block font-mono text-sm leading-6 text-slate-100">
            {children}
          </code>
        );
      }

      return (
        <code className="bg-slate-100 px-1.5 py-0.5 rounded text-sm font-mono text-slate-800">
          {children}
        </code>
      );
    },

    // Fenced code block
    pre: ({ children }) => (
      <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-4">
        {children}
      </pre>
    ),

    a: ({ href, children }) => (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline"
      >
        {children}
      </a>
    ),
  }}
>
  {msg.content}
</ReactMarkdown>
                      </div>
                    </div>
                  ))}
                  {isResponding && <span className='text-md text-gray-400 my-3 animate-pulse tracking-widest'>Responding.....</span>}

                </div>
              )}

            </div>
          </div>

          <div className="shrink-0 p-4 md:px-8 bg-slate-50">
            <div className="max-w-3xl mx-auto w-full">
              <form 
                onSubmit={handleSendMessage}
                className="relative flex items-center bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden p-1.5"
              >
                <input
                  type="text"
                  value={inputVal}
                  onChange={(e) => setInputVal(e.target.value)}
                  placeholder="Ask a question about PyTorch..."
                  className="w-full pl-4 pr-12 py-2.5 bg-transparent text-slate-900 placeholder-slate-400 focus:outline-none text-sm"
                />
                
                <button
                  type="submit"
                  disabled={isResponding}
                  className="absolute right-2 p-2 disabled:cursor-not-allowed bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors shadow-sm"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          </div>

        </main>
      </div>

    </div>
  );
}