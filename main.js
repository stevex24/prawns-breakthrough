class GameScene extends Phaser.Scene {
    constructor() {
        super("game");
    }

    preload() {
        this.load.image(
            "restaurant",
            "assets/restaurant-panel.png"
        );

        // Enable this after assets/prawn.png is added.
        this.load.image(
            "prawn",
            "assets/prawn.png"
        );
    }

    square(squareName) {
        const file =
            squareName.charCodeAt(0) -
            "a".charCodeAt(0);

        const rank = Number(squareName[1]);

        return {
            x:
                this.boardX +
                file * this.squareSize +
                this.squareSize / 2,

            y:
                this.boardY +
                (8 - rank) * this.squareSize +
                this.squareSize / 2
        };
    }

    drawBoard() {
        const graphics = this.add.graphics();

        for (let row = 0; row < 8; row++) {
            for (let column = 0; column < 8; column++) {
                const color =
                    (row + column) % 2 === 0
                        ? 0xf0d9b5
                        : 0xb58863;

                graphics.fillStyle(color);

                graphics.fillRect(
                    this.boardX + column * this.squareSize,
                    this.boardY + row * this.squareSize,
                    this.squareSize,
                    this.squareSize
                );
            }
        }

        graphics.lineStyle(3, 0x000000);

        graphics.strokeRect(
            this.boardX,
            this.boardY,
            8 * this.squareSize,
            8 * this.squareSize
        );
    }

    makePawn(squareName, color, usePrawn = false) {
        const position = this.square(squareName);

        if (usePrawn && this.textures.exists("prawn")) {
            const prawn = this.add.image(
                position.x,
                position.y,
                "prawn"
            );

            prawn.setDisplaySize(50, 50);

            // Black's prawns use the same artwork with a dark tint.
            if (color === 0x333333) {
                prawn.setTint(0x596273);
            }

            return prawn;
        }

        const pawn = this.add.circle(
            position.x,
            position.y,
            18,
            color
        );

        pawn.setStrokeStyle(2, 0x000000);

        return pawn;
    }

    makeKing(squareName, color) {
        const position = this.square(squareName);

        const king = this.add.text(
            position.x,
            position.y,
            "K",
            {
                fontSize: "36px",
                color: color,
                fontStyle: "bold"
            }
        );

        king.setOrigin(0.5);

        return king;
    }

    createPosition() {
        this.pieces = {
            whiteA: this.makePawn("a5", 0xffffff, true),
            whiteB: this.makePawn("b5", 0xffffff, true),
            whiteC: this.makePawn("c5", 0xffffff, true),

            blackA: this.makePawn("a7", 0x333333, true),
            blackB: this.makePawn("b7", 0x333333, true),
            blackC: this.makePawn("c7", 0x333333, true),

            whiteKing: this.makeKing("e1", "#ffffff"),
            blackKing: this.makeKing("e3", "#111111")
        };
    }

    destroyPosition() {
        for (const piece of Object.values(this.pieces)) {
            if (piece && piece.active) {
                piece.destroy();
            }
        }
    }

    wait(milliseconds) {
        return new Promise(resolve => {
            this.time.delayedCall(milliseconds, resolve);
        });
    }

    movePiece(piece, destination, duration = 700) {
        const target = this.square(destination);

        return new Promise(resolve => {
            // A tiny repeated rocking motion suggests comic crawling.
            const scuttle = this.tweens.add({
                targets: piece,
                angle: {
                    from: -6,
                    to: 6
                },
                duration: 110,
                yoyo: true,
                repeat: -1
            });

            this.tweens.add({
                targets: piece,
                x: target.x,
                y: target.y,
                duration: duration,
                ease: "Sine.easeInOut",

                onComplete: () => {
                    scuttle.stop();
                    piece.setAngle(0);
                    resolve();
                }
            });
        });
    }

    removePiece(piece) {
        return new Promise(resolve => {
            this.tweens.add({
                targets: piece,
                alpha: 0,
                scale: 0.4,
                duration: 250,

                onComplete: () => {
                    piece.destroy();
                    resolve();
                }
            });
        });
    }

    async playBreakthrough() {
        while (true) {
            await this.wait(700);

            // 1. b6
            await this.movePiece(
                this.pieces.whiteB,
                "b6"
            );

            await this.wait(300);

            // ...cxb6
            await this.movePiece(
                this.pieces.blackC,
                "b6"
            );

            await this.removePiece(
                this.pieces.whiteB
            );

            await this.wait(300);

            // 2. a6
            await this.movePiece(
                this.pieces.whiteA,
                "a6"
            );

            await this.wait(300);

            // ...bxa6
            await this.movePiece(
                this.pieces.blackB,
                "a6"
            );

            await this.removePiece(
                this.pieces.whiteA
            );

            await this.wait(300);

            // 3. c6
            await this.movePiece(
                this.pieces.whiteC,
                "c6"
            );

            await this.wait(1600);

            this.destroyPosition();
            this.createPosition();
        }
    }

    create() {
        this.add.text(
            24,
            18,
            "Prawn's Breakthrough — One Evening at the Checkmate Café",
            {
                fontSize: "28px",
                color: "#000000"
            }
        );

        const restaurant = this.add.image(
            275,
            365,
            "restaurant"
        );

        restaurant.setScale(0.55);

        this.boardX = 760;
        this.boardY = 100;
        this.squareSize = 60;

        this.drawBoard();
        this.createPosition();
        this.playBreakthrough();
    }
}

const config = {
    type: Phaser.AUTO,
    width: 1280,
    height: 700,
    backgroundColor: "#efe8dc",
    scene: GameScene
};

new Phaser.Game(config);
