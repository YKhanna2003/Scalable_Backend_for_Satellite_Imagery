.PHONY: clean
clean:
	del /Q image_chunks\*.png
	del /Q filtered_chunks\*.png
	del /Q combined_image.png
	del /Q chunk_ids.txt
	del /Q stacked_image_*
	del /Q "Final Image.jpg"