# Step 1: Create a new file named README.md
touch README.md

# Step 2: Write a short explanation about the project
echo " #Grayt Puzzles" > README.md
echo "" > README.md
echo "This project contains a collection of puzzles. The goal is to find the unique color asignment for which there is the asked for mate. Above the puzzles you can see what mate is asked for and how many of each color of pieces there are. It's always white to move. Below are the images of the puzzles:" > README.md

# Step 3 and 4: List all the PNG files in the grayt_puzzles directory in reverse order and add them to the README file
counter=0
for file in $(ls -r grayt_puzzles/*.png)
do
    # Extract the number of white pieces, black pieces, and moves to mate from the file name
    filename=$(basename "$file")
    puzzle=$(echo "$filename" | cut -d '_' -f 1)
    Id=$(echo "$filename" | cut -d '_' -f 2)
    mate=$(echo "$filename" | cut -d '_' -f 3)
    whitep=$(echo "$filename" | cut -d '_' -f 4)
    blackp=$(echo "$filename" | cut -d '_' -f 5 | cut -d '.' -f 1)

    # Check if the counter is even
    if [ $((counter % 2)) -eq 0 ]; then
        # Append the "Puzzle" line to the README file
        echo "## PuzzleId: $Id" >> README.md
        # Append the extracted values to the README file
        echo "$mate $whitep $blackp" >> README.md
    else
        echo "### Solution:" >> README.md
    fi


    # Check if the counter is even
    if [ $((counter % 2)) -eq 1 ]; then
        # Append the spoiler block to the README file
        echo "<details><summary>Solution $Id</summary>" >> README.md
        echo "" >> README.md
        echo "<img src=\"$file\" width=\"50%\">" >> README.md
        echo "" >> README.md
        echo "</details>" >> README.md
        echo "" >> README.md
    else
        # Append the image directly to the README file
        echo "" >> README.md
        echo "<img src=\"$file\" width=\"50%\">" >> README.md
        echo "" >> README.md
    fi

    # Increment the counter
    counter=$((counter + 1))
done