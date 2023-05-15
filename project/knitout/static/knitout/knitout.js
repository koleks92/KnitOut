const currentRoute = window.location.pathname;

if (currentRoute == "/")
{
    document.addEventListener('DOMContentLoaded', function() 
    {

    });
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
else if (currentRoute.endsWith('steps'))
{
    document.addEventListener('DOMContentLoaded', function() 
    {
        // Get all form steps and buttons
        const formSteps = document.querySelectorAll(".recipe_step");
        const prevButton = document.getElementById("recipe_step_prev");
        const nextButton = document.getElementById("recipe_step_next");

        // Set initial step and disable previous button and send button
        let currentStep = 0;
        prevButton.disabled = true;

        // Hide other views and show first
        formSteps[currentStep].style.display = "block";
        for (let i=1; i < formSteps.length; i++)
        {
            formSteps[i].style.display = "none";
        }

        // Add click event listeners to buttons
        prevButton.addEventListener("click", () => {
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
        });

        nextButton.addEventListener("click", () => {
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
            
        });       

    });
}
else if (currentRoute.startsWith("/recipe/"))
{
    document.addEventListener('DOMContentLoaded', function() 
    {
        // Get recipe id
        const id = currentRoute.replace("/recipe/", "");

        // Get thumbs_up and thumbs_down
        const thumbs_up = document.querySelector(".fa-thumbs-up");
        const thumbs_down = document.querySelector(".fa-thumbs-down");

        get_likes(thumbs_up, thumbs_down, id);

        // LIKES
        fetch(`/likes/${id}`, {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            // Check if logged
            if (data.logged)
            {
                // Get API for Likes
                thumbs_up.addEventListener('click', function() {
                    fetch(`/likes/${id}`, {
                        method: "PUT"
                    })
                    .then(response => response.json())
                    .then(data => { 
                        if (data.message == "Liked")
                        {
                            thumbs_up.classList.replace("fa-regular", "fa-solid");
                            thumbs_down.classList.replace("fa-solid", "fa-regular");
                        }
                        else if (data.message == "Unliked")
                        {
                            thumbs_up.classList.replace("fa-solid", "fa-regular");
                        }
                        get_likes(thumbs_up, thumbs_down, id);
                    })
                })

                // Get API for Dislikes
                thumbs_down.addEventListener('click', function() {
                    fetch(`/dislikes/${id}`, {
                        method: "PUT"
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message == "Disliked")
                        {
                            thumbs_down.classList.replace("fa-regular", "fa-solid");
                            thumbs_up.classList.replace("fa-solid", "fa-regular");
                        }
                        else if (data.message == "Undisliked")
                        {
                            thumbs_down.classList.replace("fa-solid", "fa-regular");
                        }
                        get_likes(thumbs_up, thumbs_down, id);
                    })
                })
            }
        });

        // FAVORITES
        fetch(`/favorites/${id}`, {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            // Check if logged
            if (data.logged)
            {
                // Get button
                const button = document.querySelector("#recipe_favorite_button");
                // If already in favorites
                if (data.favorited)
                {
                    button.innerHTML = "Remove from Favorites";
                }
                else
                {
                    button.innerHTML = "Add to Favorites";
                }


                // Get API for Dislikes
                button.addEventListener('click', function() {
                    fetch(`/favorites/${id}`, {
                        method: "PUT"
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message == "Favorited")
                        {
                            button.innerHTML = "Remove from Favorites";
                        }
                        else if (data.message == "Unfavorited")
                        {
                            button.innerHTML = "Add to Favorites";
                        }
                    })
                })
            }
        });     
    })
}

function get_likes(thumbs_up, thumbs_down, id)
{
    // Get API for GET
    fetch(`/likes/${id}`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        // Change progress and progress_bar artibutes
        const progress = document.querySelector(".progress");
        progress.ariaValueNow = data.procent_likes;
        const progress_bar = document.querySelector(".progress-bar");
        progress_bar.style = `width: ${data.procent_likes}%`;
        
        if (data.logged)
        {
            thumbs_animation(thumbs_up);
            thumbs_animation(thumbs_down);
            if (data.liked)
            {
                thumbs_up.classList.replace("fa-regular", "fa-solid");
            }
            else if (data.disliked)
            {
                thumbs_down.classList.replace("fa-regular", "fa-solid");
            }
        }
    })
}

function thumbs_animation(thumb)
{
    // Like Heart animation 
    thumb.addEventListener("mouseover", () => {
        thumb.classList.add("fa-bounce");
    });

    thumb.addEventListener("mouseout", () => {
        thumb.classList.remove("fa-bounce");
      });
}