"""
Assessment Tools - Claude Code Prompting 101
Comprehensive assessment system for validating learning outcomes.
"""

import json
import time
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class QuestionType(Enum):
    """Types of assessment questions"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    PRACTICAL = "practical"
    SCENARIO = "scenario"


class DifficultyLevel(Enum):
    """Question difficulty levels"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LearningObjective(Enum):
    """Learning objectives being assessed"""
    UNDERSTANDING = "understanding"
    APPLICATION = "application"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    EVALUATION = "evaluation"


@dataclass
class Question:
    """Assessment question structure"""
    id: str
    chapter: str
    type: QuestionType
    difficulty: DifficultyLevel
    objective: LearningObjective
    question: str
    options: List[str] = None  # For multiple choice
    correct_answer: str = ""
    explanation: str = ""
    points: int = 1
    tags: List[str] = None


@dataclass
class Assessment:
    """Complete assessment structure"""
    id: str
    title: str
    description: str
    chapters_covered: List[str]
    questions: List[Question]
    time_limit: int  # minutes
    passing_score: float  # percentage
    instructions: str


@dataclass
class StudentResponse:
    """Student's response to a question"""
    question_id: str
    answer: str
    time_spent: float  # seconds
    confidence: int  # 1-5 scale


@dataclass
class AssessmentResult:
    """Assessment results and scoring"""
    assessment_id: str
    student_id: str
    responses: List[StudentResponse]
    score: float
    percentage: float
    passed: bool
    time_taken: float
    timestamp: str
    feedback: Dict[str, Any]


class AssessmentEngine:
    """Main assessment engine for managing quizzes and evaluations"""
    
    def __init__(self):
        self.questions = self._create_question_bank()
        self.assessments = self._create_assessments()
        self.results = []
    
    def _create_question_bank(self) -> Dict[str, Question]:
        """Create comprehensive question bank"""
        
        questions = {}
        
        # Chapter 1 Questions
        questions["ch1_q1"] = Question(
            id="ch1_q1",
            chapter="01",
            type=QuestionType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BASIC,
            objective=LearningObjective.UNDERSTANDING,
            question="What is the primary purpose of prompt engineering?",
            options=[
                "To make AI models respond faster",
                "To write clear instructions that get AI models to do what we want",
                "To reduce the cost of using AI models",
                "To make AI models more creative"
            ],
            correct_answer="To write clear instructions that get AI models to do what we want",
            explanation="Prompt engineering is fundamentally about writing clear instructions for language models to get them to perform desired tasks effectively.",
            points=1,
            tags=["definition", "purpose", "fundamentals"]
        )
        
        questions["ch1_q2"] = Question(
            id="ch1_q2",
            chapter="01",
            type=QuestionType.TRUE_FALSE,
            difficulty=DifficultyLevel.BASIC,
            objective=LearningObjective.UNDERSTANDING,
            question="Prompt engineering is an exact science where you get perfect results on the first try.",
            correct_answer="False",
            explanation="Prompt engineering is an iterative, empirical science. You rarely get perfect results on the first try and must test, observe, and refine your prompts.",
            points=1,
            tags=["iterative", "empirical", "process"]
        )
        
        questions["ch1_q3"] = Question(
            id="ch1_q3",
            chapter="01",
            type=QuestionType.SCENARIO,
            difficulty=DifficultyLevel.INTERMEDIATE,
            objective=LearningObjective.APPLICATION,
            question="""You've created a prompt for analyzing customer reviews, but Claude keeps focusing on grammar instead of sentiment. What's the most likely problem and how would you fix it?""",
            correct_answer="The prompt lacks clear task context and objectives. Fix by explicitly stating the task is sentiment analysis, not grammar checking, and defining what constitutes positive/negative sentiment.",
            explanation="This demonstrates the importance of clear task context. Without explicit instructions about the analysis type, Claude may default to obvious text analysis tasks like grammar checking.",
            points=3,
            tags=["problem_solving", "task_context", "practical"]
        )
        
        # Chapter 2 Questions
        questions["ch2_q1"] = Question(
            id="ch2_q1",
            chapter="02",
            type=QuestionType.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.BASIC,
            objective=LearningObjective.UNDERSTANDING,
            question="According to the 10-point prompt structure framework, what should come first?",
            options=[
                "Examples and few-shot learning",
                "Task context and role definition",
                "Output formatting requirements",
                "Detailed step-by-step instructions"
            ],
            correct_answer="Task context and role definition",
            explanation="Task context and role definition should come first to establish the foundation for all subsequent instructions.",
            points=1,
            tags=["structure", "framework", "order"]
        )
        
        questions["ch2_q2"] = Question(
            id="ch2_q2",
            chapter="02",
            type=QuestionType.PRACTICAL,
            difficulty=DifficultyLevel.INTERMEDIATE,
            objective=LearningObjective.APPLICATION,
            question="Write a properly structured system prompt for a travel planning assistant using XML tags. Include role, task guidelines, and output requirements.",
            correct_answer="""<role>
You are a travel planning assistant helping users create personalized itineraries.
</role>

<task_guidelines>
- Research destinations based on user preferences
- Suggest activities, accommodations, and transportation
- Consider budget constraints and travel dates
- Provide practical travel advice and tips
</task_guidelines>

<output_requirements>
- Structured daily itinerary format
- Include estimated costs and time requirements
- Provide booking links or contact information where possible
- Flag any potential issues or considerations
</output_requirements>""",
            explanation="This demonstrates proper XML organization with clear sections for role definition, task guidelines, and output requirements.",
            points=5,
            tags=["xml", "structure", "practical", "system_prompt"]
        )
        
        # Chapter 3 Questions
        questions["ch3_q1"] = Question(
            id="ch3_q1",
            chapter="03",
            type=QuestionType.SHORT_ANSWER,
            difficulty=DifficultyLevel.INTERMEDIATE,
            objective=LearningObjective.ANALYSIS,
            question="Explain why confidence thresholds are important in prompt engineering and give an example of how to implement them.",
            correct_answer="Confidence thresholds prevent hallucinations and ensure reliable outputs. Example: 'Only make fault determinations when you have 80%+ confidence. If confidence is lower, state \"Insufficient evidence for determination\" and explain what additional data would help.'",
            explanation="Confidence thresholds are crucial for production systems where accuracy is more important than always providing an answer.",
            points=3,
            tags=["confidence", "reliability", "production"]
        )
        
        # Add more questions for remaining chapters...
        # (In a real implementation, this would include comprehensive coverage)
        
        return questions
    
    def _create_assessments(self) -> Dict[str, Assessment]:
        """Create different types of assessments"""
        
        assessments = {}
        
        # Chapter 1 Quiz
        ch1_questions = [q for q in self.questions.values() if q.chapter == "01"]
        assessments["ch1_quiz"] = Assessment(
            id="ch1_quiz",
            title="Chapter 1: Introduction to Prompt Engineering - Quiz",
            description="Basic knowledge check for Chapter 1 concepts",
            chapters_covered=["01"],
            questions=ch1_questions,
            time_limit=15,
            passing_score=0.7,
            instructions="Answer all questions to assess your understanding of basic prompt engineering concepts."
        )
        
        # Comprehensive Midterm
        midterm_questions = [q for q in self.questions.values() if q.chapter in ["01", "02", "03", "04"]]
        assessments["midterm"] = Assessment(
            id="midterm",
            title="Midterm Assessment: Foundations of Prompt Engineering",
            description="Comprehensive assessment covering Chapters 1-4",
            chapters_covered=["01", "02", "03", "04"],
            questions=midterm_questions,
            time_limit=60,
            passing_score=0.75,
            instructions="This assessment covers fundamental concepts from the first four chapters. Take your time and read questions carefully."
        )
        
        # Final Practical Assessment
        practical_questions = [q for q in self.questions.values() if q.objective in [LearningObjective.APPLICATION, LearningObjective.SYNTHESIS]]
        assessments["final_practical"] = Assessment(
            id="final_practical",
            title="Final Practical Assessment: Complete Prompt Engineering",
            description="Hands-on assessment requiring complete prompt creation",
            chapters_covered=["01", "02", "03", "04", "05", "06", "07", "08"],
            questions=practical_questions,
            time_limit=120,
            passing_score=0.8,
            instructions="Create complete, production-ready prompts for given scenarios. Focus on applying all course concepts."
        )
        
        return assessments
    
    def get_assessment(self, assessment_id: str) -> Optional[Assessment]:
        """Get assessment by ID"""
        return self.assessments.get(assessment_id)
    
    def start_assessment(self, assessment_id: str, student_id: str = "anonymous") -> Dict:
        """Start an assessment session"""
        assessment = self.get_assessment(assessment_id)
        if not assessment:
            return {"error": "Assessment not found"}
        
        # Randomize question order for some assessments
        questions = assessment.questions.copy()
        if assessment_id != "final_practical":  # Keep practical in logical order
            random.shuffle(questions)
        
        return {
            "assessment": assessment,
            "questions": questions,
            "start_time": time.time(),
            "student_id": student_id,
            "instructions": f"""
=== {assessment.title} ===

{assessment.description}

Instructions: {assessment.instructions}

Time Limit: {assessment.time_limit} minutes
Passing Score: {assessment.passing_score:.0%}
Number of Questions: {len(questions)}

Press Enter to begin...
            """
        }
    
    def submit_assessment(self, assessment_id: str, student_id: str, responses: List[StudentResponse], start_time: float) -> AssessmentResult:
        """Submit and score assessment"""
        assessment = self.get_assessment(assessment_id)
        if not assessment:
            raise ValueError("Assessment not found")
        
        # Calculate scoring
        total_points = sum(q.points for q in assessment.questions)
        earned_points = 0
        
        feedback = {
            "question_feedback": {},
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Score each response
        for response in responses:
            question = next((q for q in assessment.questions if q.id == response.question_id), None)
            if not question:
                continue
            
            is_correct = self._score_response(question, response)
            if is_correct:
                earned_points += question.points
            
            feedback["question_feedback"][response.question_id] = {
                "correct": is_correct,
                "your_answer": response.answer,
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
                "points_earned": question.points if is_correct else 0,
                "points_possible": question.points
            }
        
        score = earned_points / total_points if total_points > 0 else 0
        percentage = score * 100
        passed = score >= assessment.passing_score
        time_taken = time.time() - start_time
        
        # Generate feedback
        feedback.update(self._generate_assessment_feedback(assessment, responses, score))
        
        result = AssessmentResult(
            assessment_id=assessment_id,
            student_id=student_id,
            responses=responses,
            score=earned_points,
            percentage=percentage,
            passed=passed,
            time_taken=time_taken,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            feedback=feedback
        )
        
        self.results.append(result)
        return result
    
    def _score_response(self, question: Question, response: StudentResponse) -> bool:
        """Score individual response"""
        
        if question.type == QuestionType.MULTIPLE_CHOICE:
            return response.answer.strip().lower() == question.correct_answer.strip().lower()
        
        elif question.type == QuestionType.TRUE_FALSE:
            return response.answer.strip().lower() == question.correct_answer.strip().lower()
        
        elif question.type in [QuestionType.SHORT_ANSWER, QuestionType.PRACTICAL, QuestionType.SCENARIO]:
            # For open-ended questions, use keyword matching or semantic similarity
            # In a real system, this would use more sophisticated NLP
            return self._evaluate_open_response(question, response)
        
        return False
    
    def _evaluate_open_response(self, question: Question, response: StudentResponse) -> bool:
        """Evaluate open-ended responses (simplified version)"""
        
        # Extract key terms from correct answer
        correct_keywords = set(question.correct_answer.lower().split())
        response_keywords = set(response.answer.lower().split())
        
        # Simple keyword overlap scoring
        overlap = len(correct_keywords.intersection(response_keywords))
        coverage = overlap / len(correct_keywords) if correct_keywords else 0
        
        # Different thresholds for different question types
        if question.type == QuestionType.SHORT_ANSWER:
            return coverage >= 0.4  # 40% keyword overlap
        elif question.type in [QuestionType.PRACTICAL, QuestionType.SCENARIO]:
            return coverage >= 0.3  # 30% for more complex responses
        
        return False
    
    def _generate_assessment_feedback(self, assessment: Assessment, responses: List[StudentResponse], score: float) -> Dict:
        """Generate personalized feedback based on performance"""
        
        feedback = {
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Analyze performance by chapter
        chapter_performance = {}
        for response in responses:
            question = next((q for q in assessment.questions if q.id == response.question_id), None)
            if question:
                if question.chapter not in chapter_performance:
                    chapter_performance[question.chapter] = {"correct": 0, "total": 0}
                chapter_performance[question.chapter]["total"] += 1
                if self._score_response(question, response):
                    chapter_performance[question.chapter]["correct"] += 1
        
        # Generate feedback based on performance
        for chapter, perf in chapter_performance.items():
            chapter_score = perf["correct"] / perf["total"] if perf["total"] > 0 else 0
            if chapter_score >= 0.8:
                feedback["strengths"].append(f"Strong understanding of Chapter {chapter} concepts")
            elif chapter_score < 0.6:
                feedback["areas_for_improvement"].append(f"Review Chapter {chapter} material")
                feedback["recommendations"].append(f"Complete additional exercises for Chapter {chapter}")
        
        # Overall performance feedback
        if score >= 0.9:
            feedback["strengths"].append("Excellent overall performance")
        elif score >= 0.7:
            feedback["strengths"].append("Good understanding of course material")
        else:
            feedback["areas_for_improvement"].append("Fundamental concepts need reinforcement")
            feedback["recommendations"].append("Review course material and retake assessment")
        
        return feedback
    
    def generate_performance_analytics(self, student_id: str = None) -> Dict:
        """Generate performance analytics"""
        
        results = self.results
        if student_id:
            results = [r for r in results if r.student_id == student_id]
        
        if not results:
            return {"message": "No results found"}
        
        analytics = {
            "total_assessments": len(results),
            "average_score": sum(r.percentage for r in results) / len(results),
            "pass_rate": sum(1 for r in results if r.passed) / len(results),
            "assessment_breakdown": {},
            "improvement_trends": []
        }
        
        # Breakdown by assessment type
        for result in results:
            if result.assessment_id not in analytics["assessment_breakdown"]:
                analytics["assessment_breakdown"][result.assessment_id] = {
                    "attempts": 0,
                    "average_score": 0,
                    "pass_rate": 0
                }
            
            breakdown = analytics["assessment_breakdown"][result.assessment_id]
            breakdown["attempts"] += 1
            breakdown["average_score"] = (breakdown["average_score"] * (breakdown["attempts"] - 1) + result.percentage) / breakdown["attempts"]
            breakdown["pass_rate"] = sum(1 for r in results if r.assessment_id == result.assessment_id and r.passed) / breakdown["attempts"]
        
        return analytics


def interactive_assessment_session():
    """Run interactive assessment session"""
    
    engine = AssessmentEngine()
    
    print("=== Claude Code Prompting 101 Assessment System ===")
    print("Available Assessments:")
    for assessment_id, assessment in engine.assessments.items():
        print(f"  {assessment_id}: {assessment.title}")
    
    while True:
        print("\nOptions:")
        print("1. Take assessment")
        print("2. View results")
        print("3. Performance analytics")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            assessment_id = input("Enter assessment ID: ").strip()
            student_id = input("Enter your student ID (or press Enter for anonymous): ").strip() or "anonymous"
            
            session = engine.start_assessment(assessment_id, student_id)
            if "error" in session:
                print(f"Error: {session['error']}")
                continue
            
            print(session["instructions"])
            input()  # Wait for user to press Enter
            
            responses = []
            start_time = session["start_time"]
            
            for i, question in enumerate(session["questions"], 1):
                print(f"\n=== Question {i} of {len(session['questions'])} ===")
                print(f"Chapter: {question.chapter} | Difficulty: {question.difficulty.value}")
                print(f"Points: {question.points}")
                print(f"\n{question.question}")
                
                if question.options:
                    for j, option in enumerate(question.options, 1):
                        print(f"{j}. {option}")
                
                question_start = time.time()
                answer = input("\nYour answer: ").strip()
                question_time = time.time() - question_start
                
                confidence = input("Confidence (1-5, optional): ").strip()
                confidence = int(confidence) if confidence.isdigit() else 3
                
                responses.append(StudentResponse(
                    question_id=question.id,
                    answer=answer,
                    time_spent=question_time,
                    confidence=confidence
                ))
            
            # Submit and get results
            result = engine.submit_assessment(assessment_id, student_id, responses, start_time)
            
            print(f"\n=== Assessment Results ===")
            print(f"Score: {result.score}/{sum(q.points for q in session['questions'])} ({result.percentage:.1f}%)")
            print(f"Status: {'PASSED' if result.passed else 'FAILED'}")
            print(f"Time Taken: {result.time_taken/60:.1f} minutes")
            
            print(f"\nStrengths: {result.feedback.get('strengths', [])}")
            print(f"Areas for Improvement: {result.feedback.get('areas_for_improvement', [])}")
            print(f"Recommendations: {result.feedback.get('recommendations', [])}")
        
        elif choice == "2":
            if engine.results:
                print("\nRecent Results:")
                for result in engine.results[-5:]:  # Show last 5
                    print(f"{result.timestamp}: {result.assessment_id} - {result.percentage:.1f}% ({'PASS' if result.passed else 'FAIL'})")
            else:
                print("No results available.")
        
        elif choice == "3":
            analytics = engine.generate_performance_analytics()
            print(f"\nPerformance Analytics:")
            print(json.dumps(analytics, indent=2))
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    interactive_assessment_session()
