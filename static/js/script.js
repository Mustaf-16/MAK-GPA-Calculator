const courseList = document.querySelector("#course-list");
const courseTemplate = document.querySelector("#course-template");
const form = document.querySelector("#gpa-form");
const message = document.querySelector("#form-message");
const result = document.querySelector("#gpa-result");
const classification = document.querySelector("#classification-result");

function addCourse() {
	const row = courseTemplate.content.cloneNode(true);
	row.querySelector(".remove-course").addEventListener("click", (event) => {
		event.currentTarget.closest(".course-row").remove();
		if (!courseList.children.length) addCourse();
	});
	courseList.appendChild(row);
}

function readCourses() {
	return [...courseList.querySelectorAll(".course-row")].map((row) => {
		const value = row.querySelector(".course-grade").value.trim();
		const course = { credits: row.querySelector(".course-credits").value };

		if (/^\d+(\.\d+)?$/.test(value)) {
			course.mark = value;
		} else {
			course.grade = value.toUpperCase();
		}
		return course;
	});
}

document.querySelector("#add-course").addEventListener("click", addCourse);

form.addEventListener("submit", async (event) => {
	event.preventDefault();
	message.textContent = "";
	result.textContent = "...";
	classification.textContent = "Calculating...";

	try {
		const response = await fetch("/dashboard/gpa", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ courses: readCourses() }),
		});
		const data = await response.json();
		if (!response.ok) throw new Error(data.error || "Unable to calculate GPA");
		result.textContent = Number(data.gpa).toFixed(2);
		classification.textContent = data.classification;
	} catch (error) {
		result.textContent = "--";
		classification.textContent = "Calculate to see your class";
		message.textContent = error.message;
	}
});

addCourse();
