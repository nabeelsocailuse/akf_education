frappe.ready(function () {
    
  // bind events here
})


// frappe.ready(function () {
//   frappe.web_form.validate = () => { 
//     const academic_year = frappe.web_form.get_value("academic_year");
//     const program = frappe.web_form.get_value("program");
//     const dobStr = frappe.web_form.get_value("date_of_birth1");

//     if (!dobStr) {
//       frappe.throw("Please enter your Date of Birth.");
//       return false;  // Stop form submission
//     }

//     if (!academic_year || !program) {
//       frappe.throw("Please select both Academic Year and Program.");
//       return false;  // Stop form submission
//     }

//     const age = calculateAge(dobStr);

//     // Fetch program criteria
//     fetchProgramDetails(academic_year, program).then((programDetails) => {
//       if (!programDetails) {
//         frappe.throw("Program age criteria not found.");
//         return false;  // Stop form submission
//       }

//       const minAge = programDetails.min_age;
//       const maxAge = programDetails.max_age;

//       console.log("Your age is:", age);
//       console.log("Min Age:", minAge, "Max Age:", maxAge);

//       if (age < minAge) {
//         frappe.throw(`Your age is ${age} — it's less than the program's minimum age of ${minAge}.`);
//         return false;  // Stop form submission
//       } else if (age > maxAge) {
//         frappe.throw(`Your age is ${age} — it's higher than the program's maximum age of ${maxAge}.`);
//         return false;  // Stop form submission
//       }

//     });

//     return false;  
//   };
// });

// function calculateAge(dobStr) {
//   const dob = new Date(dobStr);
//   const today = new Date();

//   let age = today.getFullYear() - dob.getFullYear();
//   const m = today.getMonth() - dob.getMonth();
//   if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
//     age--;
//   }
//   return age;
// }

// function fetchProgramDetails(academic_year, program) {
//   return new Promise((resolve, reject) => {
//     frappe.call({
//       method: "akf_education.akf_education.web_form.student_applicant.student_applicant.get_student_admission_program_details",
//       args: {
//         academic_year: academic_year,
//         program: program
//       },
//       callback: function (r) {
//         if (r.message && r.message.length) {
//           resolve(r.message[0]);
//         } else {
//           resolve(null);
//         }
//       }
//     });
//   });
// }



