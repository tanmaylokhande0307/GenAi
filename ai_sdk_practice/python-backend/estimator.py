from typing import Annotated,Any, List, Optional,TypedDict, Sequence
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
import numpy as np
import pandas as pd
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool

df = pd.read_csv("data/agent_data.csv")
uniqueJobNames = df['Name'].unique()
uniqueJobCategories = df['Category'].unique()

class EstimatorInput(BaseModel):
    Name: str = Field(description="Name of the job")
    Category: str = Field(description="Category of the job")
    NewCount: int = Field(description="Number of new jobs")
    SaveAsCount: Optional[str] = Field(
        default=0, 
        description="This is an optional field with a default value"
    )
    CloneCount: Optional[str] = Field(
        default=0, 
        description="This is an optional field with a default value"
    )
    
class EstimatorOutput(BaseModel):
    TotalNewhrs: np.float64 = Field(description="Total hours required to complete the new job")
    TotalSaveAshrs: Optional[np.float64] = Field(
        default=0, 
        description="Total hours required to complete the Saveas job"
    )
    TotalClonehrs: Optional[np.float64] = Field(
        default=0, 
        description="Total hours required to complete the clone job"
    )

@tool(return_direct=False,args_schema=EstimatorInput)
def estimatorTool(Name: str, Category: str, NewCount: int, SaveAsCount: int = 0, CloneCount: int = 0) -> EstimatorOutput:
    """Estimator tool to give the estimate i.e time required to complete the job based on input parameters such as Name, category, NewCount, SaveAsCount, CloneCount"""
    print(Name,Category)
    filtered_df = df[(df['Name'] == Name) & (df['Category'] == Category)]
    NewHrsPerJob = filtered_df["NewPerJob"].values[0]
    SaveAsHrsPerJob = filtered_df["SaveAsPerJob"].values[0]
    CloneHrsPerJob =  filtered_df["ClonePerJob"].values[0]
    
    TotalNewhrs = np.float64(NewCount) * NewHrsPerJob
    TotalSaveAshrs = np.float64(SaveAsCount) * SaveAsHrsPerJob
    
    result = {
        'TotalNewhrs': TotalNewhrs,
        'TotalSaveAshrs': TotalSaveAshrs
    }

    if Category == "TeklaModelling" and CloneCount != 0:
        TotalClonehrs = np.float64(CloneCount) * CloneHrsPerJob
        result['TotalClonehrs'] = TotalClonehrs

    return result

def is_valid_estimator_input(obj):
    if not isinstance(obj, dict):
        return False, "The object is not a dictionary."
    
    if 'Name' not in obj or obj.get('Name') not in uniqueJobNames:
        print("Invalid Name")
        return False,f"Missing required field: Name"
    
    if 'Category' not in obj or obj.get('Category') not in uniqueJobCategories:
        print("Invalid Category")
        return False,f"Missing required field: Category"

    if 'NewCount' not in obj:
        print("NewCount")
        return False,f"Missing required field: NewCount"
    
    return True, "The object is valid."

# ans = estimatorTool.invoke({'Name': 'External Wall Sandwich Panel', 'Category': 'TeklaModelling', 'NewCount': 44, 'SaveAsCount': '44', 'CloneCount': '59'})
# print(ans)
# estimatorTool = StructuredTool.from_function(
#     func=get_estimate,
#     name="Estimator",
#     description="Estimate the total time to complete a job",
#     args_schema=EstimatorInput,
#     return_direct=False,
# )

