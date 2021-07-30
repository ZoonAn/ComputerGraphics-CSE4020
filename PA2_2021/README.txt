global variables:
	inputState: counts left-clicks to set the points for the cow.
	inputLocation: an array to save 6 positions where the cow was clicked.
	inputDone: if the six positions are set, changed to True and start the animation of the cow.
	animationStartTime: for saving the moment inputDone is changed to True.
	cowRotationPos: for calculating the rotation of the cow.

new functions:
	getBSpline(t, p0, p1, p2, p3): calculates the point of B-Spline of the 4 points p0, p1, p2, and p3. Uses cubic B-Spline.
	setCowRotation(directionVec): gets the normal direction vector of the cow, and rotate the cow to face the direction.

changed functions:
	display(): while inputState < 6, draw cows on the selected positions. When inputState reaches 6, calulate the position of the cow on the B-spline with getBSpline() function, and set the direction cow should face with setCowRotation() function.
		Translate the cowRotationPos to the position on the B-spline, and draw the cow. after the cow goes around the B-spline 3 times, set inputState, inputLocation, inputDone to initial state, and the cow stay at the last position.
	onMouseButtion(window, button, state, mods): down-click of the left mouse button sets the drag mode to V_DRAG. 
		If left mouse button goes up, set the drag to H_DRAG, increase inputState by 1, and save the location to inputLocation. if it was the sixth input, set animationStartTime, and inputDone to True.
	onMouseDrag(window, x, y): if the drag mode is V_DRAG, create a plane perpendicular to the floor on the position of the cow, and get the y coordinate only and translate the position.