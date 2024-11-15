#parse.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the global prompt template once
PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the AI model once
model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks, parse_description):
    """
    Parse DOM chunks using the Ollama model and extract specific information.

    :param dom_chunks: List of DOM content chunks (strings) to parse.
    :param parse_description: The description of what information to extract.
    :return: The parsed results as a single string.
    """
    logger.info("Starting parsing process with %d chunks.", len(dom_chunks))
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            # Format the prompt with the chunk and description
            prompt = PROMPT_TEMPLATE.format(
                dom_content=chunk,
                parse_description=parse_description
            )
            logger.info("Parsing chunk %d/%d", i, len(dom_chunks))

            # Directly pass the formatted string to the model
            response = model.invoke(prompt)

            # Log the response
            logger.info("Successfully parsed chunk %d/%d", i, len(dom_chunks))
            parsed_results.append(response)
        except Exception as e:
            logger.error("Error parsing chunk %d: %s", i, str(e))
            parsed_results.append("")  # Append an empty string for failed chunks

    logger.info("Parsing process completed.")
    return "\n".join(parsed_results)
