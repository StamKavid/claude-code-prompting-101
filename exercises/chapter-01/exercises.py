"""
Chapter 1 Exercises: Introduction to Prompt Engineering
Claude Code Prompting 101

Interactive exercises to practice fundamental prompt engineering concepts.
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ExerciseLevel(Enum):
    """Exercise difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"


class AssessmentCriteria(Enum):
    """Assessment criteria for exercises"""
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    STRUCTURE = "structure"
    PRACTICALITY = "practicality"


@dataclass
class Exercise:
    """Individual exercise definition"""
    id: str
    title: str
    level: ExerciseLevel
    objectives: List[str]
    description: str
    sample_scenario: str
    success_criteria: List[str]
    time_estimate: int  # minutes
    assessment_rubric: Dict[AssessmentCriteria, str]


@dataclass
class ExerciseSubmission:
    """Student exercise submission"""
    exercise_id: str
    student_response: str
    timestamp: str
    self_assessment: Dict[str, int]  # 1-5 scale


class Chapter1Exercises:
    """Chapter 1 exercise collection and management"""
    
    def __init__(self):
        self.exercises = self._create_exercises()
        self.submissions = []
    
    def _create_exercises(self) -> Dict[str, Exercise]:
        """Create Chapter 1 exercises"""
        
        return {
            "1.1": Exercise(
                id="1.1",
                title="Basic Prompt Construction",
                level=ExerciseLevel.BEGINNER,
                objectives=[
                    "Construct a basic prompt for a specific task",
                    "Identify the core components of effective prompts",
                    "Recognize common prompt construction mistakes"
                ],
                description="""
You work for a medical clinic that wants to use AI to help categorize patient symptoms 
from intake forms. Create a basic prompt that instructs Claude to:
1. Read patient symptom descriptions
2. Categorize symptoms into body systems (respiratory, digestive, etc.)
3. Flag urgent symptoms that need immediate attention

Write your initial prompt attempt without looking at the course materials.
                """,
                sample_scenario="""
Patient intake form:
"I've been having severe chest pain for the last 2 hours, especially when I breathe. 
Also experiencing shortness of breath and some nausea. Pain radiates to my left arm."
                """,
                success_criteria=[
                    "Prompt clearly defines the task",
                    "Instructions are specific enough to guide categorization",
                    "Includes mechanism for flagging urgent symptoms",
                    "Can be understood by someone unfamiliar with medical terminology"
                ],
                time_estimate=20,
                assessment_rubric={
                    AssessmentCriteria.CLARITY: "Instructions are clear and unambiguous",
                    AssessmentCriteria.COMPLETENESS: "All required components addressed", 
                    AssessmentCriteria.STRUCTURE: "Logical organization of instructions",
                    AssessmentCriteria.PRACTICALITY: "Prompt would work in real scenarios"
                }
            ),
            
            "1.2": Exercise(
                id="1.2", 
                title="Problem Identification in Naive Prompts",
                level=ExerciseLevel.BEGINNER,
                objectives=[
                    "Analyze problematic prompts and identify specific issues",
                    "Understand why vague prompts lead to poor results",
                    "Practice systematic prompt evaluation"
                ],
                description="""
Analyze the following problematic prompts and identify specific issues with each.
For each prompt, list 3-5 specific problems and explain why each problem would
lead to poor or inconsistent results.
                """,
                sample_scenario="""
Problematic Prompt #1:
"Look at this legal document and tell me what it says."

Problematic Prompt #2: 
"Analyze this data and give me insights."

Problematic Prompt #3:
"Help me write something professional for work."
                """,
                success_criteria=[
                    "Identifies vagueness and lack of specificity",
                    "Recognizes missing context and domain information",
                    "Points out absence of output format requirements",
                    "Understands how ambiguity leads to inconsistent results"
                ],
                time_estimate=15,
                assessment_rubric={
                    AssessmentCriteria.CLARITY: "Issues are clearly articulated",
                    AssessmentCriteria.COMPLETENESS: "Multiple problems identified per prompt",
                    AssessmentCriteria.STRUCTURE: "Systematic analysis approach",
                    AssessmentCriteria.PRACTICALITY: "Problems connect to real consequences"
                }
            ),
            
            "1.3": Exercise(
                id="1.3",
                title="Iterative Improvement Process",
                level=ExerciseLevel.INTERMEDIATE,
                objectives=[
                    "Practice the iterative improvement methodology",
                    "Document prompt evolution through versions",
                    "Apply empirical testing approach to prompt development"
                ],
                description="""
Take your basic prompt from Exercise 1.1 and improve it through 3 iterations.
For each iteration:
1. Test the prompt with the provided scenarios
2. Identify specific problems with the output
3. Make targeted improvements
4. Document what changed and why

Create versions 1.0, 2.0, and 3.0 of your medical symptom categorization prompt.
                """,
                sample_scenario="""
Test scenarios:
1. "Severe chest pain, shortness of breath, arm pain"  
2. "Mild headache, occasional dizziness, tired lately"
3. "Stomach pain after eating, some nausea, bloated feeling"
4. "Rash on arms, itchy, started after new medication"
5. "Can't sleep, anxious about work, heart racing sometimes"
                """,
                success_criteria=[
                    "Three distinct prompt versions created",
                    "Each iteration shows specific improvements",
                    "Problems and solutions clearly documented",
                    "Final version significantly better than initial",
                    "Testing results justify changes made"
                ],
                time_estimate=45,
                assessment_rubric={
                    AssessmentCriteria.CLARITY: "Evolution process clearly documented",
                    AssessmentCriteria.COMPLETENESS: "All iterations completed with testing",
                    AssessmentCriteria.STRUCTURE: "Systematic improvement methodology",
                    AssessmentCriteria.PRACTICALITY: "Improvements address real issues"
                }
            )
        }
    
    def get_exercise(self, exercise_id: str) -> Optional[Exercise]:
        """Get specific exercise by ID"""
        return self.exercises.get(exercise_id)
    
    def list_exercises(self) -> List[str]:
        """List all available exercises"""
        return [f"{ex.id}: {ex.title} ({ex.level.value})" for ex in self.exercises.values()]
    
    def start_exercise(self, exercise_id: str) -> Dict:
        """Start an exercise session"""
        exercise = self.get_exercise(exercise_id)
        if not exercise:
            return {"error": "Exercise not found"}
        
        return {
            "exercise": exercise,
            "start_time": time.time(),
            "instructions": f"""
=== {exercise.title} ===
Level: {exercise.level.value.title()}
Estimated Time: {exercise.time_estimate} minutes

Objectives:
{chr(10).join(f"- {obj}" for obj in exercise.objectives)}

Description:
{exercise.description}

Sample Scenario:
{exercise.sample_scenario}

Success Criteria:
{chr(10).join(f"- {criteria}" for criteria in exercise.success_criteria)}

Begin your response below:
            """
        }
    
    def submit_exercise(self, exercise_id: str, response: str, self_assessment: Dict[str, int] = None) -> Dict:
        """Submit exercise response"""
        exercise = self.get_exercise(exercise_id)
        if not exercise:
            return {"error": "Exercise not found"}
        
        submission = ExerciseSubmission(
            exercise_id=exercise_id,
            student_response=response,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            self_assessment=self_assessment or {}
        )
        
        self.submissions.append(submission)
        
        # Generate feedback
        feedback = self._generate_feedback(exercise, submission)
        
        return {
            "submission_received": True,
            "timestamp": submission.timestamp,
            "feedback": feedback,
            "next_steps": self._get_next_steps(exercise_id)
        }
    
    def _generate_feedback(self, exercise: Exercise, submission: ExerciseSubmission) -> Dict:
        """Generate feedback for exercise submission"""
        
        # This would integrate with actual assessment in a real system
        feedback = {
            "completion_status": "submitted",
            "areas_to_review": [],
            "strengths": [],
            "suggestions": []
        }
        
        # Analyze response length and structure
        response_length = len(submission.student_response)
        if response_length < 100:
            feedback["areas_to_review"].append("Response may be too brief for complete analysis")
        elif response_length > 2000:
            feedback["areas_to_review"].append("Consider being more concise and focused")
        
        # Check for key elements based on exercise
        if exercise.id == "1.1":
            if "symptom" not in submission.student_response.lower():
                feedback["areas_to_review"].append("Ensure your prompt addresses symptom categorization")
            if "urgent" not in submission.student_response.lower():
                feedback["areas_to_review"].append("Include mechanism for flagging urgent symptoms")
        
        # General feedback
        feedback["suggestions"].extend([
            "Compare your response with the success criteria",
            "Consider how your prompt would perform with edge cases",
            "Review the sample scenario to ensure your prompt addresses it"
        ])
        
        return feedback
    
    def _get_next_steps(self, completed_exercise_id: str) -> List[str]:
        """Get recommended next steps after completing exercise"""
        
        exercise_order = ["1.1", "1.2", "1.3"]
        
        try:
            current_index = exercise_order.index(completed_exercise_id)
            if current_index < len(exercise_order) - 1:
                next_exercise = exercise_order[current_index + 1]
                return [
                    f"Proceed to Exercise {next_exercise}",
                    "Review your submission against the assessment rubric",
                    "Compare your approach with provided solutions"
                ]
            else:
                return [
                    "Complete Chapter 1 assessment quiz",
                    "Proceed to Chapter 2: Prompt Structure Fundamentals",
                    "Review all Chapter 1 exercises for patterns"
                ]
        except ValueError:
            return ["Continue with remaining Chapter 1 exercises"]
    
    def generate_progress_report(self) -> Dict:
        """Generate progress report for all exercises"""
        
        completed = [sub.exercise_id for sub in self.submissions]
        total_exercises = len(self.exercises)
        completion_rate = len(completed) / total_exercises
        
        return {
            "total_exercises": total_exercises,
            "completed_exercises": len(completed),
            "completion_rate": f"{completion_rate:.1%}",
            "completed_list": completed,
            "remaining_exercises": [ex_id for ex_id in self.exercises.keys() if ex_id not in completed],
            "estimated_time_remaining": sum(
                self.exercises[ex_id].time_estimate 
                for ex_id in self.exercises.keys() 
                if ex_id not in completed
            )
        }


def interactive_exercise_session():
    """Run interactive exercise session"""
    
    exercises = Chapter1Exercises()
    
    print("=== Chapter 1: Introduction to Prompt Engineering ===")
    print("Available Exercises:")
    for exercise_info in exercises.list_exercises():
        print(f"  {exercise_info}")
    
    while True:
        print("\nOptions:")
        print("1. Start exercise")
        print("2. View progress")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            exercise_id = input("Enter exercise ID (e.g., 1.1): ").strip()
            session = exercises.start_exercise(exercise_id)
            
            if "error" in session:
                print(f"Error: {session['error']}")
                continue
            
            print(session["instructions"])
            
            print("\nEnter your response (type 'DONE' on a new line when finished):")
            response_lines = []
            while True:
                line = input()
                if line.strip() == "DONE":
                    break
                response_lines.append(line)
            
            response = "\n".join(response_lines)
            
            # Optional self-assessment
            print("\nOptional self-assessment (1-5 scale, press Enter to skip):")
            self_assessment = {}
            for criteria in ["clarity", "completeness", "structure", "practicality"]:
                score = input(f"{criteria.title()} (1-5): ").strip()
                if score.isdigit():
                    self_assessment[criteria] = int(score)
            
            result = exercises.submit_exercise(exercise_id, response, self_assessment)
            print(f"\nSubmission Status: {result['submission_received']}")
            print(f"Feedback: {json.dumps(result['feedback'], indent=2)}")
            print(f"Next Steps: {result['next_steps']}")
        
        elif choice == "2":
            progress = exercises.generate_progress_report()
            print(f"\nProgress Report:")
            print(f"Completed: {progress['completed_exercises']}/{progress['total_exercises']} ({progress['completion_rate']})")
            print(f"Estimated time remaining: {progress['estimated_time_remaining']} minutes")
            
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    interactive_exercise_session()
