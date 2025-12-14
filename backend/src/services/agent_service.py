"""
OpenAI Agents SDK-based RAG chatbot service for the Physical AI textbook.
Uses OpenAI Agents SDK with Gemini as the LLM provider via OpenAI-compatible endpoint.
Implements proper RAG by pre-fetching context from vector database.
"""
import json
from typing import List, Dict, Optional, AsyncGenerator, Annotated
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from src.services.embedding_service import EmbeddingService
from src.services.vector_store_service import VectorStoreService
from src.services.db_service import db_service
from src.core.config import settings

# Disable tracing for cleaner output
set_tracing_disabled(True)

# Course navigation map for redirect functionality with section anchors
COURSE_NAVIGATION = {
    # Main pages
    "intro": {"path": "/docs", "title": "Introduction"},
    "introduction": {"path": "/docs", "title": "Introduction"},
    "home": {"path": "/docs", "title": "Introduction"},
    
    # Week-specific navigation (all 13 weeks)
    "week 1": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Week 1: Introduction to Physical AI"},
    "week1": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Week 1: Introduction to Physical AI"},
    "week 2": {"path": "/docs/module1/week2-intro-physical-ai-2", "title": "Week 2: Sensors and Embodiment"},
    "week2": {"path": "/docs/module1/week2-intro-physical-ai-2", "title": "Week 2: Sensors and Embodiment"},
    "week 3": {"path": "/docs/module1/week3-ros-fundamentals", "title": "Week 3: ROS 2 Architecture"},
    "week3": {"path": "/docs/module1/week3-ros-fundamentals", "title": "Week 3: ROS 2 Architecture"},
    "week 4": {"path": "/docs/module1/week4-ros-fundamentals-2", "title": "Week 4: ROS 2 Communication"},
    "week4": {"path": "/docs/module1/week4-ros-fundamentals-2", "title": "Week 4: ROS 2 Communication"},
    "week 5": {"path": "/docs/module1/week5-ros-fundamentals-3", "title": "Week 5: ROS 2 Packages"},
    "week5": {"path": "/docs/module1/week5-ros-fundamentals-3", "title": "Week 5: ROS 2 Packages"},
    "week 6": {"path": "/docs/module2/week6-gazebo", "title": "Week 6: Gazebo Simulation"},
    "week6": {"path": "/docs/module2/week6-gazebo", "title": "Week 6: Gazebo Simulation"},
    "week 7": {"path": "/docs/module2/week7-gazebo-unity", "title": "Week 7: Unity Integration"},
    "week7": {"path": "/docs/module2/week7-gazebo-unity", "title": "Week 7: Unity Integration"},
    "week 8": {"path": "/docs/module3/week8-isaac", "title": "Week 8: Isaac Platform Overview"},
    "week8": {"path": "/docs/module3/week8-isaac", "title": "Week 8: Isaac Platform Overview"},
    "week 9": {"path": "/docs/module3/week9-isaac-2", "title": "Week 9: Isaac ROS and VSLAM"},
    "week9": {"path": "/docs/module3/week9-isaac-2", "title": "Week 9: Isaac ROS and VSLAM"},
    "week 10": {"path": "/docs/module3/week10-isaac-3", "title": "Week 10: Sim-to-Real Transfer"},
    "week10": {"path": "/docs/module3/week10-isaac-3", "title": "Week 10: Sim-to-Real Transfer"},
    "week 11": {"path": "/docs/module4/week11-humanoid-dev", "title": "Week 11: Humanoid Kinematics"},
    "week11": {"path": "/docs/module4/week11-humanoid-dev", "title": "Week 11: Humanoid Kinematics"},
    "week 12": {"path": "/docs/module4/week12-humanoid-dev-2", "title": "Week 12: Manipulation"},
    "week12": {"path": "/docs/module4/week12-humanoid-dev-2", "title": "Week 12: Manipulation"},
    "week 13": {"path": "/docs/module4/week13-conversational-robotics", "title": "Week 13: Conversational Robotics"},
    "week13": {"path": "/docs/module4/week13-conversational-robotics", "title": "Week 13: Conversational Robotics"},
    
    # Module 1: ROS 2 Fundamentals
    "module 1": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Module 1: ROS 2 Fundamentals"},
    "module1": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Module 1: ROS 2 Fundamentals"},
    "ros": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Module 1: ROS 2 Fundamentals"},
    "ros 2": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Module 1: ROS 2 Fundamentals"},
    "ros2": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Module 1: ROS 2 Fundamentals"},
    "physical ai": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Introduction to Physical AI"},
    "embodied intelligence": {"path": "/docs/module1/week1-intro-physical-ai#the-physics-why", "title": "Embodied Intelligence"},
    "sensors": {"path": "/docs/module1/week2-intro-physical-ai-2", "title": "Sensors and Embodiment"},
    "lidar": {"path": "/docs/module1/week2-intro-physical-ai-2#lidar-sensors", "title": "LIDAR Sensors"},
    "imu": {"path": "/docs/module1/week2-intro-physical-ai-2#imu-sensors", "title": "IMU Sensors"},
    "nodes": {"path": "/docs/module1/week3-ros-fundamentals#ros-2-nodes", "title": "ROS 2 Nodes"},
    "topics": {"path": "/docs/module1/week4-ros-fundamentals-2#topics-and-messages", "title": "ROS 2 Topics"},
    "services": {"path": "/docs/module1/week4-ros-fundamentals-2#services", "title": "ROS 2 Services"},
    "launch files": {"path": "/docs/module1/week5-ros-fundamentals-3#launch-files", "title": "ROS 2 Launch Files"},
    
    # Module 2: Gazebo & Unity
    "module 2": {"path": "/docs/module2/week6-gazebo", "title": "Module 2: Gazebo & Unity"},
    "module2": {"path": "/docs/module2/week6-gazebo", "title": "Module 2: Gazebo & Unity"},
    "gazebo": {"path": "/docs/module2/week6-gazebo", "title": "Module 2: Gazebo & Unity"},
    "unity": {"path": "/docs/module2/week7-gazebo-unity", "title": "Unity Integration"},
    "simulation": {"path": "/docs/module2/week6-gazebo", "title": "Module 2: Gazebo & Unity"},
    "digital twin": {"path": "/docs/module2/week6-gazebo", "title": "Module 2: Gazebo & Unity"},
    "urdf": {"path": "/docs/module2/week6-gazebo#urdf-robot-description", "title": "URDF Robot Description"},
    "sdf": {"path": "/docs/module2/week6-gazebo#sdf-format", "title": "SDF Format"},
    "physics simulation": {"path": "/docs/module2/week6-gazebo#physics-simulation", "title": "Physics Simulation"},
    
    # Module 3: NVIDIA Isaac
    "module 3": {"path": "/docs/module3/week8-isaac", "title": "Module 3: NVIDIA Isaac"},
    "module3": {"path": "/docs/module3/week8-isaac", "title": "Module 3: NVIDIA Isaac"},
    "isaac": {"path": "/docs/module3/week8-isaac", "title": "Module 3: NVIDIA Isaac"},
    "nvidia": {"path": "/docs/module3/week8-isaac", "title": "Module 3: NVIDIA Isaac"},
    "nvidia isaac": {"path": "/docs/module3/week8-isaac", "title": "Module 3: NVIDIA Isaac"},
    "isaac sim": {"path": "/docs/module3/week8-isaac#isaac-sim-setup", "title": "Isaac Sim Setup"},
    "vslam": {"path": "/docs/module3/week9-isaac-2#vslam", "title": "Visual SLAM"},
    "sim to real": {"path": "/docs/module3/week10-isaac-3#sim-to-real-transfer", "title": "Sim-to-Real Transfer"},
    "domain randomization": {"path": "/docs/module3/week10-isaac-3#domain-randomization", "title": "Domain Randomization"},
    
    # Module 4: Vision-Language-Action
    "module 4": {"path": "/docs/module4/week11-humanoid-dev", "title": "Module 4: Vision-Language-Action"},
    "module4": {"path": "/docs/module4/week11-humanoid-dev", "title": "Module 4: Vision-Language-Action"},
    "vla": {"path": "/docs/module4/week13-conversational-robotics", "title": "Module 4: Vision-Language-Action"},
    "conversational": {"path": "/docs/module4/week13-conversational-robotics", "title": "Module 4: Conversational Robotics"},
    "humanoid": {"path": "/docs/module4/week11-humanoid-dev", "title": "Humanoid Development"},
    "kinematics": {"path": "/docs/module4/week11-humanoid-dev#kinematics", "title": "Humanoid Kinematics"},
    "locomotion": {"path": "/docs/module4/week11-humanoid-dev#bipedal-locomotion", "title": "Bipedal Locomotion"},
    "manipulation": {"path": "/docs/module4/week12-humanoid-dev-2", "title": "Manipulation and Interaction"},
    "grasping": {"path": "/docs/module4/week12-humanoid-dev-2#grasping", "title": "Grasping"},
    "gpt": {"path": "/docs/module4/week13-conversational-robotics#gpt-integration", "title": "GPT Integration"},
    "whisper": {"path": "/docs/module4/week13-conversational-robotics#voice-to-action", "title": "Voice to Action"},
    "voice": {"path": "/docs/module4/week13-conversational-robotics#voice-to-action", "title": "Voice Commands"},
    
    # Numeric shortcuts for modules
    "1": {"path": "/docs/module1/week1-intro-physical-ai", "title": "Module 1: ROS 2 Fundamentals"},
    "2": {"path": "/docs/module2/week6-gazebo", "title": "Module 2: Gazebo & Unity"},
    "3": {"path": "/docs/module3/week8-isaac", "title": "Module 3: NVIDIA Isaac"},
    "4": {"path": "/docs/module4/week11-humanoid-dev", "title": "Module 4: Vision-Language-Action"},
    
    # Common sections (can be used with any module)
    "learning outcomes": {"path": "#learning-outcomes", "title": "Learning Outcomes", "is_anchor_only": True},
    "assessments": {"path": "#assessments", "title": "Assessments", "is_anchor_only": True},
    "code": {"path": "#the-code-how", "title": "Code Examples", "is_anchor_only": True},
    "hardware": {"path": "#the-hardware-reality", "title": "Hardware Requirements", "is_anchor_only": True},
}


# Define the navigation tool as a function tool
@function_tool
def navigate_to_page(
    destination: Annotated[str, "The page, module, week, or topic to navigate to. Examples: 'week 9', 'module 3', 'vslam', 'kinematics'"],
    section: Annotated[str, "Optional section anchor within the page. Examples: 'learning-outcomes', 'the-code-how', 'assessments'"] = ""
) -> str:
    """
    Navigate the user to a specific page or section in the Physical AI textbook.
    Use this tool when the user asks to go to, navigate to, redirect to, find, or open a specific page, module, week, or topic.
    
    Available destinations include:
    - Weeks: 'week 1' through 'week 13' (e.g., 'week 9' for Isaac ROS and VSLAM)
    - Modules: 'module 1', 'module 2', 'module 3', 'module 4' (or just '1', '2', '3', '4')
    - Topics: 'ros', 'gazebo', 'isaac', 'vla', 'humanoid', 'sensors', 'nodes', 'topics'
    - Specific content: 'kinematics', 'vslam', 'grasping', 'whisper', 'urdf', 'sdf'
    - Sections: 'learning outcomes', 'assessments', 'code', 'hardware'
    
    Week to Module mapping:
    - Weeks 1-5: Module 1 (ROS 2)
    - Weeks 6-7: Module 2 (Gazebo & Unity)
    - Weeks 8-10: Module 3 (NVIDIA Isaac)
    - Weeks 11-13: Module 4 (VLA)
    
    The tool will highlight the target section when the user arrives at the page.
    """
    destination_lower = destination.lower().strip()
    section_lower = section.lower().strip() if section else ""
    
    # Try to find matching navigation
    if destination_lower in COURSE_NAVIGATION:
        nav_info = COURSE_NAVIGATION[destination_lower]
        path = nav_info["path"]
        
        # Handle anchor-only entries (like "learning outcomes")
        if nav_info.get("is_anchor_only"):
            return json.dumps({
                "action": "anchor_only",
                "anchor": path,
                "title": nav_info["title"],
                "message": f"Scroll to {nav_info['title']} section on the current page"
            })
        
        # Add section anchor if provided and path doesn't already have one
        if section_lower and "#" not in path:
            # Convert section to anchor format
            anchor = section_lower.replace(" ", "-").replace("_", "-")
            path = f"{path}#{anchor}"
        
        return json.dumps({
            "action": "redirect",
            "path": path,
            "title": nav_info["title"],
            "message": f"Navigating to {nav_info['title']}"
        })
    
    # Try partial matching for more flexible navigation
    best_match = None
    best_score = 0
    
    for key, nav_info in COURSE_NAVIGATION.items():
        # Skip anchor-only entries for partial matching
        if nav_info.get("is_anchor_only"):
            continue
            
        # Calculate match score
        score = 0
        if key in destination_lower:
            score = len(key) * 2  # Exact substring match
        elif destination_lower in key:
            score = len(destination_lower)  # Partial match
        
        # Check for word matches
        dest_words = set(destination_lower.split())
        key_words = set(key.split())
        common_words = dest_words & key_words
        score += len(common_words) * 3
        
        if score > best_score:
            best_score = score
            best_match = (key, nav_info)
    
    if best_match and best_score > 0:
        key, nav_info = best_match
        path = nav_info["path"]
        
        # Add section anchor if provided
        if section_lower and "#" not in path:
            anchor = section_lower.replace(" ", "-").replace("_", "-")
            path = f"{path}#{anchor}"
        
        return json.dumps({
            "action": "redirect",
            "path": path,
            "title": nav_info["title"],
            "message": f"Navigating to {nav_info['title']}"
        })
    
    # No match found - provide helpful suggestions
    available_modules = "module 1 (ROS 2), module 2 (Gazebo), module 3 (Isaac), module 4 (VLA)"
    available_topics = "sensors, nodes, topics, urdf, vslam, kinematics, grasping, whisper"
    return json.dumps({
        "action": "error",
        "message": f"Could not find '{destination}'. Try: {available_modules}. Or topics: {available_topics}"
    })


@function_tool
def list_available_pages() -> str:
    """
    List all available pages and modules in the Physical AI textbook.
    Use this tool when the user asks what pages are available or wants to see the course structure.
    """
    pages = [
        {"title": "Introduction", "path": "/docs", "description": "Course overview and getting started"},
        # Module 1
        {"title": "Module 1: ROS 2 Fundamentals", "path": "/docs/module1/week1-intro-physical-ai", "description": "The Robotic Nervous System"},
        {"title": "Week 1: Introduction to Physical AI", "path": "/docs/module1/week1-intro-physical-ai", "description": "Foundations of embodied intelligence"},
        {"title": "Week 2: Sensors and Embodiment", "path": "/docs/module1/week2-intro-physical-ai-2", "description": "LIDAR, cameras, IMUs"},
        {"title": "Week 3: ROS 2 Architecture", "path": "/docs/module1/week3-ros-fundamentals", "description": "Nodes, topics, services"},
        {"title": "Week 4: ROS 2 Communication", "path": "/docs/module1/week4-ros-fundamentals-2", "description": "Publishers, subscribers"},
        {"title": "Week 5: ROS 2 Packages", "path": "/docs/module1/week5-ros-fundamentals-3", "description": "Launch files, parameters"},
        # Module 2
        {"title": "Module 2: Gazebo & Unity", "path": "/docs/module2/week6-gazebo", "description": "The Digital Twin"},
        {"title": "Week 6: Gazebo Simulation", "path": "/docs/module2/week6-gazebo", "description": "Physics simulation, URDF/SDF"},
        {"title": "Week 7: Unity Integration", "path": "/docs/module2/week7-gazebo-unity", "description": "Sensor simulation"},
        # Module 3
        {"title": "Module 3: NVIDIA Isaac", "path": "/docs/module3/week8-isaac", "description": "The AI-Robot Brain"},
        {"title": "Week 8: Isaac Platform Overview", "path": "/docs/module3/week8-isaac", "description": "Isaac SDK and Sim setup"},
        {"title": "Week 9: Isaac ROS and VSLAM", "path": "/docs/module3/week9-isaac-2", "description": "Visual SLAM, perception"},
        {"title": "Week 10: Sim-to-Real Transfer", "path": "/docs/module3/week10-isaac-3", "description": "Domain randomization"},
        # Module 4
        {"title": "Module 4: Vision-Language-Action", "path": "/docs/module4/week11-humanoid-dev", "description": "LLMs meet Robotics"},
        {"title": "Week 11: Humanoid Kinematics", "path": "/docs/module4/week11-humanoid-dev", "description": "Bipedal locomotion"},
        {"title": "Week 12: Manipulation", "path": "/docs/module4/week12-humanoid-dev-2", "description": "Grasping, interaction"},
        {"title": "Week 13: Conversational Robotics", "path": "/docs/module4/week13-conversational-robotics", "description": "GPT, Whisper integration"},
    ]
    return json.dumps({"pages": pages})


class TextbookAgent:
    """Agent for answering questions about the Physical AI textbook using OpenAI Agents SDK with Gemini."""
    
    def __init__(self):
        # Use Gemini's OpenAI-compatible endpoint
        self.client = AsyncOpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url=settings.GEMINI_BASE_URL
        )
        # Create OpenAI Agents SDK model with Gemini backend
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=self.client
        )
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
    
    def _search_textbook(self, query: str) -> str:
        """Search the textbook for relevant content with navigation hints."""
        try:
            embedding = self.embedding_service.get_embedding(query)
            results = self.vector_store_service.search_vectors(embedding, limit=8)
            
            if not results:
                return "No relevant content found in the textbook."
            
            context = "TEXTBOOK CONTENT:\n\n"
            for i, result in enumerate(results, 1):
                # Clean up source file path for display
                source = result['source_file']
                if 'physical-ai-textbook' in source:
                    source = source.split('physical-ai-textbook')[-1].replace('\\', '/')
                
                # Extract navigation path from source file
                nav_path = self._source_to_nav_path(source)
                
                context += f"--- Source {i}: {source} (Relevance: {result['score']:.2f}) ---\n"
                if nav_path:
                    context += f"[Navigation: {nav_path}]\n"
                context += f"{result['text']}\n\n"
            
            return context
        except Exception as e:
            return f"Error searching textbook: {str(e)}"
    
    def _source_to_nav_path(self, source: str) -> str:
        """Convert a source file path to a navigation path for the chatbot."""
        # Extract module and week from path like /docs/docs/module1/week1-intro-physical-ai.md
        import re
        
        # Base URL for GitHub Pages deployment
        base_url = "/physical-ai-and-humanoid-robotics"
        
        # Match patterns like module1/week1-intro-physical-ai.md
        match = re.search(r'(module\d+)/([^/]+)\.md', source)
        if match:
            module = match.group(1)
            page = match.group(2)
            return f"{base_url}/docs/{module}/{page}"
        
        # Match intro.md
        if 'intro.md' in source:
            return f"{base_url}/docs"
        
        return ""
    
    def _get_user_context(self, user_id: Optional[str]) -> str:
        """Get user's background for personalization."""
        if not user_id:
            return ""
        
        try:
            user = db_service.get_user_by_id(user_id)
            if not user or not user.get('background'):
                return ""
            
            background = user['background']
            context = f"\nUSER CONTEXT:\n"
            context += f"- Name: {user.get('name', 'Unknown')}\n"
            context += f"- Programming Experience: {background.get('programming_experience', 'unknown')}\n"
            context += f"- Robotics Experience: {background.get('robotics_experience', 'unknown')}\n"
            context += f"- Preferred Languages: {', '.join(background.get('preferred_languages', []))}\n"
            context += f"- Hardware Access: {', '.join(background.get('hardware_access', []))}\n"
            
            return context
        except Exception as e:
            return ""
    
    def _get_system_prompt(self, textbook_context: str, user_context: str, current_page: Optional[str]) -> str:
        """Build dynamic system prompt with retrieved context."""
        prompt = """You are an expert assistant for the Physical AI & Humanoid Robotics textbook.
You have access to tools that allow you to navigate users to different pages in the textbook.

Your role is to help students learn about:
- Module 1: ROS 2 (Robot Operating System) - The Robotic Nervous System
- Module 2: Gazebo & Unity - The Digital Twin (physics simulation and environment building)
- Module 3: NVIDIA Isaac - The AI-Robot Brain (advanced perception and training)
- Module 4: Vision-Language-Action (VLA) - The convergence of LLMs and Robotics

IMPORTANT - NAVIGATION TOOL USAGE:
When a user asks to be redirected, navigate, go to, or open a specific page or module, you MUST use the navigate_to_page tool.
Examples of when to use the navigation tool:
- "redirect me to module 3"
- "take me to the ROS section"
- "go to the introduction"
- "navigate to gazebo"
- "open module 2"
- "show me the isaac page"

When you use the navigate_to_page tool, include the tool's response in your answer so the frontend can process the redirect.

RESPONSE LENGTH GUIDELINES:
- By DEFAULT, provide CONCISE, focused answers (2-4 paragraphs)
- Only provide DETAILED, comprehensive answers when the user explicitly asks for:
  - "in depth", "detailed", "comprehensive", "explain thoroughly", "tell me more", "elaborate"
- For simple questions, give direct answers without excessive elaboration

CRITICAL INSTRUCTIONS:
1. Base your answers primarily on the TEXTBOOK CONTENT provided below
2. Use markdown formatting for readability (headers, bullets, code blocks)
3. Reference specific sources when relevant
4. Include code examples only when directly relevant or requested
5. Tailor explanations to the user's experience level when user context is available
6. ALWAYS use the navigate_to_page tool when users ask to go to a specific page

RESPONSE FORMAT:
- Use ## headers for sections (only for detailed responses)
- Use bullet points for lists
- Use `code` for inline code and ```language for code blocks
- Keep responses scannable and well-organized

"""
        if current_page:
            prompt += f"\nUSER IS CURRENTLY VIEWING: {current_page}\n"
        
        if user_context:
            prompt += f"\n{user_context}\n"
        
        prompt += f"\n{textbook_context}\n"
        
        prompt += """
When answering:
- Reference specific sources and modules from the textbook content above
- Adapt complexity based on user's background if available
- Provide detailed, helpful explanations
- Include practical examples and code snippets when relevant
- Use the navigate_to_page tool when users want to go to a specific page"""
        
        return prompt
    
    async def chat_stream(
        self, 
        user_message: str, 
        history: List[Dict[str, str]], 
        selected_text: Optional[str] = None,
        user_id: Optional[str] = None,
        current_page: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response from the agent using OpenAI Agents SDK with proper RAG.
        
        Args:
            user_message: The user's question
            history: Previous conversation turns
            selected_text: Optional text selected by user from documentation
            user_id: User ID for personalization
            current_page: Current page URL for context
        """
        # Build search query
        search_query = user_message
        if selected_text:
            search_query = f"{user_message} {selected_text[:500]}"
        
        # Pre-fetch context from vector database
        textbook_context = self._search_textbook(search_query)
        user_context = self._get_user_context(user_id)
        
        # Build dynamic system prompt with context
        system_prompt = self._get_system_prompt(textbook_context, user_context, current_page)
        
        # Create agent with dynamic instructions and tools
        agent = Agent(
            name="Physical AI Textbook Assistant",
            instructions=system_prompt,
            model=self.model,
            tools=[navigate_to_page, list_available_pages],  # Add navigation tools
        )
        
        # Build user message
        enhanced_message = user_message
        if selected_text:
            enhanced_message += f"\n\n[User selected this text from the page: {selected_text}]"
        
        full_response = []
        
        try:
            # Use OpenAI Agents SDK Runner to execute the agent
            result = await Runner.run(
                agent,
                input=enhanced_message
            )
            
            # Get the final output
            response_text = result.final_output
            
            # Check if any tool was called and include redirect info
            for item in result.new_items:
                if hasattr(item, 'output') and item.output:
                    try:
                        tool_output = json.loads(item.output)
                        if tool_output.get('action') == 'redirect':
                            # Append redirect marker to response
                            response_text += f"\n\n[[REDIRECT:{tool_output['path']}]]"
                            break
                    except (json.JSONDecodeError, TypeError):
                        pass
            
            full_response.append(response_text)
            
            # Yield the response
            yield response_text
            
            # Log the interaction
            db_service.log_chat_interaction(
                user_message=user_message,
                ai_response="".join(full_response),
                source_documents=[]
            )
            
        except Exception as e:
            error_msg = f"\n\n**Error:** {str(e)}. Please try again."
            yield error_msg
            db_service.log_chat_interaction(
                user_message=user_message,
                ai_response=f"Error: {str(e)}",
                source_documents=[]
            )


# Singleton instance
textbook_agent = TextbookAgent()
