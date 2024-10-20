import serial  # pyserial for serial communication
import pygame
import math

# Initialize serial communication
ser = serial.Serial('COM5', 9600)

# Initialize pygame for graphics
pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sonar Radar')

# Set some variables
iAngle = 0
iDistance = 0
running = True

def draw_radar():
    # Draw radar arcs
    for r in range(200, 600, 100):
        pygame.draw.arc(screen, (98, 245, 31), (width//2-r, height-r, 2*r, 2*r), math.pi, 2*math.pi, 2)

    # Draw radar lines
    for angle in range(0, 180, 30):
        x = (width//2) + math.cos(math.radians(angle)) * 600
        y = (height) - math.sin(math.radians(angle)) * 600
        pygame.draw.line(screen, (98, 245, 31), (width//2, height), (x, y), 2)

def draw_object(iAngle, iDistance):
    if iDistance < 40:  # Limit the range to 40 cm
        pixsDistance = iDistance * (height * 0.025)
        x = width//2 + pixsDistance * math.cos(math.radians(iAngle))
        y = height - pixsDistance * math.sin(math.radians(iAngle))
        pygame.draw.line(screen, (255, 10, 10), (width//2, height), (x, y), 9)

# Main loop
while running:
    screen.fill((0, 0, 0))  # Clear screen
    draw_radar()
    
    # Serial data reading and parsing
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()  # Read data
        if ',' in data:
            angle, distance = data.split(',')
            iAngle = int(angle)
            iDistance = int(distance)
    
    draw_object(iAngle, iDistance)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()  # Refresh screen

pygame.quit()
