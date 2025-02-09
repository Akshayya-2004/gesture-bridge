const API_BASE_URL="http://127.0.0.1:5000"

export const getGesture=async()=>{
    try{
        const response=await fetch(`${API_BASE_URL}/detect`);
        return response;
    }
    catch(error){
        console.error("Error in fetching gesture: ", error);
    }
};
