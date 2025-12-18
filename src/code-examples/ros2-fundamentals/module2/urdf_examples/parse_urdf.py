import xml.etree.ElementTree as ET
import os

def parse_urdf(urdf_file_path):
    """
    Parses a URDF file and extracts information about links and joints.
    This is a simplified example without full URDF model loading/validation.
    """
    if not os.path.exists(urdf_file_path):
        print(f"Error: URDF file not found at {urdf_file_path}")
        return

    tree = ET.parse(urdf_file_path)
    root = tree.getroot()

    print(f"Robot Name: {root.get('name')}")
    print("\n--- Links ---")
    for link in root.findall('link'):
        name = link.get('name')
        inertial = link.find('inertial')
        mass = inertial.find('mass').get('value') if inertial and inertial.find('mass') else 'N/A'
        print(f"  Link Name: {name}, Mass: {mass}")

    print("\n--- Joints ---")
    for joint in root.findall('joint'):
        name = joint.get('name')
        joint_type = joint.get('type')
        parent = joint.find('parent').get('link') if joint.find('parent') else 'N/A'
        child = joint.find('child').get('link') if joint.find('child') else 'N/A'
        origin = joint.find('origin').get('xyz') if joint.find('origin') else 'N/A'
        axis = joint.find('axis').get('xyz') if joint.find('axis') else 'N/A'
        print(f"  Joint Name: {name}, Type: {joint_type}, Parent: {parent}, Child: {child}, Origin: {origin}, Axis: {axis}")

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    urdf_file = os.path.join(script_dir, 'simple_robot.urdf')
    parse_urdf(urdf_file)
