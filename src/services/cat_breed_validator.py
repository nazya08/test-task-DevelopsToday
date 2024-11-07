import requests
from fastapi import HTTPException

from src.main.config import settings


class CatBreedValidator:
    def __init__(self):
        self.api_key = settings.CAT_API_KEY
        self.breeds = self.fetch_breeds()

    def fetch_breeds(self) -> dict:
        """
        Fetch the list of breeds from TheCatAPI and return a dictionary with breed IDs as keys.
        """
        url = "https://api.thecatapi.com/v1/breeds"
        headers = {"x-api-key": self.api_key}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching cat breeds.")

        # Convert the list of breeds into a dictionary for quick lookup
        breeds = {breed["id"]: breed["name"] for breed in response.json()}
        return breeds

    def validate_breed(self, breed_id: str) -> bool:
        """
        Validate if the given breed_id exists in TheCatAPI breed list.
        """
        if breed_id not in self.breeds:
            raise HTTPException(status_code=400, detail="Invalid cat breed.")
        return True


cat_breed_validator = CatBreedValidator()
