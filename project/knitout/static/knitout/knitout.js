const currentRoute = window.location.pathname;

if (currentRoute === "/")
{
    console.log("index");
}
else if (currentRoute.startsWith('/add_recipe/'))
{
    document.addEventListener('DOMContentLoaded', function() 
    {
        // Get all form steps and buttons
        const formSteps = document.querySelectorAll(".add_step");
        const prevButton = document.getElementById("add_step_prev");
        const nextButton = document.getElementById("add_step_next");
        const sendButton = document.getElementById("add_steps_button");
        
        // Set initial step and disable previous button and send button
        let currentStep = 0;
        prevButton.disabled = true;
        sendButton.disabled = true;


        // Hide other views and show first
        formSteps[currentStep].style.display = "block";
        for (let i=1; i < formSteps.length; i++)
        {
            formSteps[i].style.display = "none";
        }

        // Check if all steps have a value
        const checkAllSteps = () => {
            for (let i = 0; i < formSteps.length; i++) {
                const textarea = formSteps[i].querySelector("textarea");
                if (textarea.value.trim() === "") {
                    return false;
                }
            }
            return true;
        };

        // Add keyup event listeners to textareas
        formSteps.forEach((step) => {
            const textarea = step.querySelector("textarea");
            textarea.addEventListener("keyup", (event) => {
                sendButton.disabled = !checkAllSteps();
            });
        });
        
        // Add click event listeners to buttons
        prevButton.addEventListener("click", (event) => {
            event.preventDefault();

            // Hide current step
            formSteps[currentStep].style.display = "none";
            // Decrement step and show previous step
            currentStep--;
            formSteps[currentStep].style.display = "block";
            // Disable previous button if on first step
            if (currentStep === 0) {
                prevButton.disabled = true;
            }
            // Enable next button if previously disabled
            if (nextButton.disabled) {
                nextButton.disabled = false;
            }
            
            sendButton.disabled = !checkAllSteps();

        });

        nextButton.addEventListener("click", (event) => {
            event.preventDefault();

            // Hide current step
            formSteps[currentStep].style.display = "none";
            // Increment step and show next step
            currentStep++;
            formSteps[currentStep].style.display = "block";
            // Disable next button if on last step
            if (currentStep === formSteps.length - 1) {
                nextButton.disabled = true;
            }
            // Enable previous button if previously disabled
            if (prevButton.disabled) {
                prevButton.disabled = false;
            }
            
            sendButton.disabled = !checkAllSteps();


        });

        
    })  
}