import os
import random
from azure.ai.vision.face import FaceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face.models import FaceAttributeType, FaceDetectionModel, FaceRecognitionModel

class ArtifactScanner:
    def __init__(self):
        # Check .env for mode
        self.simulation = os.getenv("SIMULATION_MODE", "True") == "True"
        
        if not self.simulation:
            # Load Real Keys
            endpoint = os.getenv("AZURE_FACE_ENDPOINT")
            key = os.getenv("AZURE_FACE_KEY")
            
            if not endpoint or not key:
                print("⚠️ ERROR: Azure Keys missing in .env! Reverting to Simulation.")
                self.simulation = True
            else:
                try:
                    self.client = FaceClient(endpoint, AzureKeyCredential(key))
                    print("👁️ VISUAL DEFENSE: Connected to Real Azure AI.")
                except Exception as e:
                    print(f"⚠️ Connection Failed: {e}")
                    self.simulation = True
        
        if self.simulation:
            print("👁️ VISUAL DEFENSE: Running in Simulation Mode.")

    def scan_video_feed(self, video_url):
        print(f"   [Scanner] Analyzing feed: {video_url[:30]}...")

        if self.simulation:
            return self._simulate_detection()
        else:
            return self._real_azure_scan(video_url)

    def _simulate_detection(self):
        # Simulation Logic (Keep this for demos without internet)
        is_threat = random.choice([True, False])
        if is_threat:
            return {"status": "THREAT_DETECTED", "reason": "Simulated Deepfake Artifacts"}
        return {"status": "SAFE", "reason": "Simulation: Biometrics Verified"}

    # UPDATE THIS METHOD INSIDE ArtifactScanner CLASS
    def _real_azure_scan(self, image_input):
        try:
            print(f"   [Azure] Uploading image to Cloud AI...")
            
            # Open the local file and send the bits to Azure
            with open(image_input, "rb") as image_stream:
                result = self.client.detect(
                    image_content=image_stream.read(), # <--- THIS IS THE MAGIC CHANGE
                    detection_model=FaceDetectionModel.DETECTION_03,
                    recognition_model=FaceRecognitionModel.RECOGNITION_04,
                    return_face_attributes=[FaceAttributeType.HEAD_POSE, FaceAttributeType.MASK]
                )

            if not result:
                return {"status": "THREAT_DETECTED", "reason": "No Face Detected"}
            
            face = result[0]
            if face.face_attributes.mask.type != "noMask":
                 return {"status": "THREAT_DETECTED", "reason": "Face Obstructed / Mask Detected"}

            return {"status": "SAFE", "reason": "Real Human Face Detected"}

        except Exception as e:
            print(f"❌ Azure Error: {e}")
            # Fallback to simulation if Azure fails
            return self._simulate_detection()