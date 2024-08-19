import sqlite3

def add_departments():
    departments = [
        ["Orthopedic Surgery - Joint Replacement (Hip, Knee, Shoulder)"],
        ["Orthopedic Surgery - Spine Surgery"],
        ["Orthopedic Surgery - Arthroscopy and Sports Medicine"],
        ["Orthopedic Surgery - Hand Surgery"],
        ["Orthopedic Surgery - Foot and Ankle Surgery"],
        ["Orthopedic Surgery - Trauma and Fracture Care"],
        ["Rheumatology - Diagnosis and treatment of arthritis and autoimmune diseases"],
        ["Pain Management - Chronic pain management"],
        ["Pain Management - Pain relief therapies"],
        ["Physiotherapy and Rehabilitation - Post-surgery rehabilitation"],
        ["Physiotherapy and Rehabilitation - Physical therapy for musculoskeletal disorders"],
        ["Pediatric Orthopedics - Treatment of orthopedic conditions in children"],
        ["Orthopedic Oncology - Management of bone and soft tissue tumors"],
        ["Sports Medicine - Treatment of sports-related injuries"],
        ["Sports Medicine - Performance enhancement programs"],
        ["Bone Health and Osteoporosis Clinic - Diagnosis and treatment of osteoporosis"],
        ["Bone Health and Osteoporosis Clinic - Bone density testing"],
        ["Orthopedic Trauma Care - Emergency services for fractures and injuries"],
        ["Geriatric Orthopedics - Orthopedic care for the elderly"],
        ["Spine Care Center - Comprehensive spine care and surgery"],
        ["Occupational Therapy - Therapy to help patients return to daily activities"],
        ["Orthopedic Research and Education - Research on new treatments and techniques"],
        ["Orthopedic Research and Education - Training programs for orthopedic professionals"],
        ["Radiology and Imaging - X-rays, MRIs, and CT scans for diagnosis"],
        ["Orthopedic Outpatient Services - Consultation and minor procedures"],
        ["Anesthesia and Pain Clinic - Preoperative and postoperative anesthesia care"]
    ]
    for i in range(0, 26, 1):
        departments[i].append(i+1)
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO departments (name, id) VALUES (?, ?)", [(department, id,) for [department, id] in departments])
        conn.commit()

if __name__ == '__main__':
    add_departments()
    print("Departments added successfully.")
