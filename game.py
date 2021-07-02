from pygame.locals import *
import random
import pygame
import sys
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# PYGAME SETTING AND VARIABLEs
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

FPS = 30
FramePerSec = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CATCH THE BLOCK")

# Game State
START_GAME = False
PLAYER_X = 320
PLAYER_Y = 400
SIZE_PLAYER_X = 100
SIZE_PLAYER_Y = 10
SIZE_BLOCK_X = 50
SIZE_BLOCK_Y = 50
BLOCK_X = random.randint(0, (SCREEN_WIDTH-50))
BLOCK_Y = 0
SPEED_Y = 7
SCORE = 0
COLOR_PLAYER = (92, 60, 146)
COLOR_BLOCK = (30, 132, 127)
COLOR_TEXT = (255, 255, 255)

Player = pygame.Rect(PLAYER_X, PLAYER_Y, SIZE_PLAYER_X, SIZE_PLAYER_Y)
Enemy = pygame.Rect(BLOCK_X, BLOCK_Y, SIZE_BLOCK_X, SIZE_BLOCK_Y)


# Video Capture and Hand Detection
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Check if the User wants to PLAY or QUIT the GAME
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            # Resetting the Game State
            START_GAME = True
            PLAYER_X = 320
            PLAYER_Y = 400
            SIZE_PLAYER_X = 100
            SIZE_PLAYER_Y = 10
            SIZE_BLOCK_X = 50
            SIZE_BLOCK_Y = 50
            BLOCK_X = random.randint(0, (SCREEN_WIDTH-50))
            BLOCK_Y = 0
            SPEED_Y = 7
            SCORE = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Only Draw the Player when the START_GAME is True
                if START_GAME is True:
                    x = hand_landmarks.landmark[8].x
                    y = hand_landmarks.landmark[8].y
                    z = hand_landmarks.landmark[8].z
                    PLAYER_X = x*SCREEN_WIDTH
                    Player = pygame.Rect(
                        PLAYER_X, PLAYER_Y, SIZE_PLAYER_X, SIZE_PLAYER_Y)
                    pygame.draw.rect(screen, COLOR_PLAYER, Player)
                    pygame.display.flip()
                # Draw Hand LandMarks
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Check if the Game is started by User
        if START_GAME is True:
            BLOCK_Y += SPEED_Y
            Block = pygame.Rect(BLOCK_X, BLOCK_Y, SIZE_BLOCK_X, SIZE_BLOCK_Y)
            pygame.draw.rect(screen, COLOR_BLOCK, Block)
            if Player.colliderect(Block):
                # Update SCORE each time Player catches the BLOCK
                SCORE += 1
                SPEED_Y += 1
                SIZE_PLAYER_X -= 1
                BLOCK_X = random.randint(0, (SCREEN_WIDTH-50))
                BLOCK_Y = 0
            if(BLOCK_Y > SCREEN_HEIGHT):
                # STOP the Game if the BLOCK is not catched by Player
                BLOCK_X = random.randint(0, (SCREEN_WIDTH-50))
                BLOCK_Y = 0
                pygame.display.update()
                START_GAME = False
            else:
                pygame.display.update()
                screen.fill((0, 0, 0))
                # Display SCORE on opencv
                cv2.putText(image, f'SCORE : {SCORE}',
                            (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, COLOR_TEXT, 2)

        else:
            # Display SCORE and START GAME MESSAGE
            cv2.putText(image, f'PRESS SPACE TO START THE GAME',
                        (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TEXT, 2)
            if SCORE:
                cv2.putText(image, f'SCORE : {SCORE}',
                            (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TEXT, 2)
        cv2.imshow('CATCH THE BLOCK !', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
pygame.quit()
