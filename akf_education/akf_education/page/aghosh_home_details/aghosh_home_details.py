import frappe
@frappe.whitelist()
def get_aghosh_home_dashboard(filters=None):
    # total_students = frappe.db.count("Student")
    # students_in_shilter = frappe.db.count("Program Enrollment", filters={"bed": ["!=", ""]})
    # sponsored_childrens = frappe.db.sql("""SELECT COUNT(DISTINCT student_id)
    #             FROM `tabSponsorship`
    #             WHERE ifnull(donor_id,"")!="";
    #             """)[0][0] or 0

    return {

        # "total_students": total_students,
        # "students_in_shilter": students_in_shilter,
        # "sponsored_childrens": sponsored_childrens,
        # "unsponsored_childrens": (total_students - sponsored_childrens),
        # "activity_pictures": student_activity_pictures(),
        # "activity_videos": student_activity_videos(),
        # "drawing_activity": student_activity_drawing(),
        # "APRs": APRs_count(),
        # "student_with_psychological_assessment": student_with_psychological_assessment(),
        # "charts_data": {
        #     "aghosh_homes_interval_count": num_of_aghosh_homes_present(),
        #     "aghosh_home_status": get_aghosh_home_status(),
        #     "childens_registration": childens_registration_intervals(),
        #     "aprs_data": aprs_count(),
        #     "operational_home": operational_home(),
        #     "under_counstruction": under_counstruction_home(),
        #     "inactive": inactive_home(),
        # },
        # "aghosh_home_locations": get_aghosh_home_locations()  
    }


# @frappe.whitelist()
# def get_aghosh_home_status():
#     result = frappe.db.sql("""
#         SELECT status, COUNT(status) as total
#         FROM `tabAghosh Home`
#         WHERE docstatus = 0 AND IFNULL(status, '') != ''
#         GROUP BY status
#         ORDER BY status
#     """, as_dict=True)
#     return result

# @frappe.whitelist()
# def num_of_aghosh_homes_present():
#     data = frappe.db.sql("""
#         SELECT
#             YEAR(Established_Date) AS Year, 
#             COUNT(*) AS aghosh_home
#         FROM 
#             `tabAghosh Home`
#         WHERE
#             Established_Date IS NOT NULL
#         GROUP BY 
#             YEAR(Established_Date)
#         ORDER BY 
#             YEAR(Established_Date) ASC;
#     """, as_dict=True)
#     return data

# @frappe.whitelist()
# def aprs_count():
#     data = frappe.db.sql("""
#         SELECT
#             pe.academic_year,
#             COUNT(DISTINCT pe.student) AS total_enrolled_students,
#             (
#                 SELECT COUNT(DISTINCT ar.student)
#                 FROM `tabAssessment Result` ar
#                 WHERE ar.academic_year = pe.academic_year
#                 AND ar.select_term = 'Final Term'
#                 AND ar.docstatus = 1
#             ) AS total_final_term_results_submitted
#         FROM `tabProgram Enrollment` pe
#         WHERE pe.docstatus = 1
#         GROUP BY pe.academic_year
#         ORDER BY pe.academic_year DESC
#     """, as_dict=True)

#     return data