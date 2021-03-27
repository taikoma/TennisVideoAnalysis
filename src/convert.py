
import database
import score
import track_data


if __name__ == "__main__":
    score=score.Score(0)
    filename="./data/nishikori-medvedev.db"
    db=database.Database(filename,score)
    db.load_database()
    score=db.db2score()

    track_data=track_data.TrackData()

    track_filename="./data/track-data2.csv"
    track_data.load_track_data(track_filename)

    track_data.load_track_to_score(score)
    print("score.array_x1",score.array_x1)

    save_filename="./data/add_track.db"
    db = database.Database(save_filename, score)
    db.save_database()

    

