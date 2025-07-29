import frappe
@frappe.whitelist()
def get_aghosh_home_dashboard(aghosh_home_id=None):

    # students_in_shilter = frappe.db.count("Program Enrollment", filters={"bed": ["!=", ""]})
    sponsored_childrens = frappe.db.sql("""SELECT COUNT(DISTINCT student_id)
                FROM `tabSponsorship`
                WHERE ifnull(donor_id,"")!="" and aghosh_home_id = %s
                AND docstatus = 1
            """, (aghosh_home_id,), as_list=True)[0][0] or 0
    return {
        "aghosh_home_name": frappe.db.get_value("Aghosh Home", aghosh_home_id, "aghosh_home_name") if aghosh_home_id else None,
        "total_students": total_students(aghosh_home_id),
        "total_beds": total_beds(aghosh_home_id),
        "total_rooms": total_rooms(aghosh_home_id),
        "sponsored_childrens": sponsored_childrens,
        "total_cameras": total_cameras(aghosh_home_id),
        "active_cameras": active_cameras(aghosh_home_id),
        "inactive_cameras": inactive_cameras(aghosh_home_id),
        "disabled_students": disabled_students(aghosh_home_id),
        "children_with_glasses": children_with_glasses(aghosh_home_id),
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

@frappe.whitelist()
def total_students(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id})

@frappe.whitelist()
def total_beds(aghosh_home_id=None):
    return frappe.db.count("Beds", filters={"aghosh_home_id": aghosh_home_id})

@frappe.whitelist()
def total_rooms(aghosh_home_id=None):
    return frappe.db.count("Rooms", filters={"aghosh_home_id": aghosh_home_id})

@frappe.whitelist()
def total_cameras(aghosh_home_id=None):
    return frappe.db.get_value("Aghosh Home", aghosh_home_id, "total_cameras") or 0

@frappe.whitelist()
def active_cameras(aghosh_home_id=None):
    return frappe.db.get_value("Aghosh Home", aghosh_home_id, "active_camera_count") or 0

@frappe.whitelist()
def inactive_cameras(aghosh_home_id=None):
    return frappe.db.get_value("Aghosh Home", aghosh_home_id, "inactive_camera_count") or 0

@frappe.whitelist()
def disabled_students(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "disabled_child": "Yes"})

@frappe.whitelist()
def children_with_glasses(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "wear_glasses": "Yes"})

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