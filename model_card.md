# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeFinder 1.0**

A content-based music recommender that scores songs against a user taste profile and returns the top matches from a small catalog.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeFinder is designed for classroom exploration only. It is not a real product and should not be used to make recommendations for actual users.

It takes a user's favorite genre, favorite mood, target energy level, and whether they like acoustic music. Then it scores every song in the catalog against those preferences and returns the top 5 matches with a plain-language explanation for each one.

It assumes the user already knows what genre and mood they want, and that their taste does not change between sessions. It should NOT be used for real music recommendations, for users with complex or changing taste, or as a replacement for platforms like Spotify or Apple Music.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song in the catalog gets a score based on how well it matches the user. The scoring works in two layers.

The first layer checks for exact matches on genre and mood. A genre match is worth 3 points and a mood match is worth 2 points. Genre is worth more because getting the genre wrong feels the most off to a listener, even if everything else is right.

The second layer looks at numbers. For energy, the system checks how far the song's energy is from the user's target and awards up to 2 points (closer is always better, not louder or faster). For acousticness it does the same thing for up to 1 point. For valence, which measures how happy or dark a song sounds, the system guesses the target based on the user's favorite mood and awards up to 1 point.

The maximum score is 9.0. Once every song has a score, the system sorts them and returns the top 5. A song with the right genre and mood starts with up to 5 points before any numbers are even checked, so it almost always wins.

The main change from the starter logic was adding valence and acousticness to the scoring, and raising the genre weight from 2.0 to 3.0 after testing showed that a 2:1 ratio between genre and mood did not create enough separation between candidates.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs. It started with 10 from the project starter and I added 8 more to cover genres and moods that were missing.

Each song has 10 attributes: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. For scoring I only use genre, mood, energy, acousticness, and valence. Tempo and danceability were left out because they were redundant with energy in this small dataset.

The 18 songs cover 15 genres (pop, lofi, rock, jazz, ambient, synthwave, hip-hop, classical, r&b, metal, folk, EDM, soul, reggae, indie pop) and 14 moods (happy, chill, intense, relaxed, moody, focused, energetic, melancholic, romantic, angry, nostalgic, euphoric, sad, uplifting).

What is missing: 13 of the 15 genres have only one song, so there is almost no variety within a genre. Only 2 songs out of 18 have a mid-range energy between 0.5 and 0.7. The data also does not include lyrics, language, release year, or cultural context, and it mostly reflects one person's taste choices rather than a wide range of listeners.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best when the user's preferences line up clearly with what is in the catalog. For users who like lofi, the results felt the most natural: three lofi songs filled the top 3 with the right moods in the right order.

The scoring is also easy to understand and explain. Every recommendation comes with a list of reasons showing exactly which features matched and how many points each contributed. A user can trace exactly why a song was recommended.

The system separates very different users well. When comparing the rock fan and the lofi listener, not a single song appeared in both top-5 lists because the energy gap between those two profiles is large enough to pull the results completely apart.

The results are also stable and predictable, which made testing straightforward. Running the same profile twice always gives the same result.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users

The biggest weakness I found is what I am calling the "one-song genre trap." Because 13 out of 15 genres in the catalog only have a single song, the genre bonus (+3.0 points) basically guarantees that the same song will always come out on top for any user whose favorite genre matches, no matter what else they prefer. For example, when I tested a user who likes rock music but also wants acoustic songs, the system still recommended Storm Runner as the #1 result even though Storm Runner scored almost zero on acousticness, because the genre and mood bonuses together were just too high to overcome. This means the system creates a filter bubble where certain users will get the exact same recommendation every single time with no variety at all, which is the opposite of what a good recommender should do. I also found a mid-energy dead zone in the data: only 2 out of 18 songs have an energy level between 0.5 and 0.7, so users who prefer moderate-energy music are basically ignored by the scoring because there is nothing close to their target in the catalog. If I were to fix this, I would either add more songs per genre so the numeric features actually get a chance to separate candidates, or I would lower the genre weight so that emotional signals like mood and valence have more influence over the final ranking.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested six different user profiles to see whether the recommender gave results that actually made sense. Three of them were "standard" profiles with preferences that match songs in the catalog well: a high-energy rock fan, a chill lofi listener, and an upbeat pop dancer. The other three were designed to be tricky on purpose, including a user who wanted sad EDM, a user who listed a genre that does not exist in the catalog at all (country), and a user who likes rock but also wants acoustic music.

For the standard profiles the results felt right almost every time. The lofi listener got three lofi songs in a row at the top, and the pop dancer's number one pick was Sunrise City, which is the only song that matches both pop genre and happy mood at the same time.

The results that surprised me most came from the tricky profiles. The sad EDM user got Drop Zone, which is a euphoric high-energy track, as the top result because the genre matched. The system had no way to understand that a sad person probably does not want a euphoric song because the genre bonus was strong enough to override the mood signal completely. The acoustic rocker also surprised me: even though that user said they like acoustic music, Storm Runner (one of the least acoustic songs in the catalog) still came in at number one because genre and mood together gave it too many points to lose. I also ran a weight experiment where I cut the genre bonus in half and doubled the energy weight, but the same songs mostly came out on top anyway, which showed me the real problem is not the weights but how few songs exist per genre.

---

### Profile Pair Comparisons

**Profile A (rock/intense) vs Profile B (lofi/chill)**

These two profiles are basically complete opposites, and the recommendations reflected that clearly. Profile A got Storm Runner at the top with a score of 8.72, while Profile B got Library Rain at 8.80. What is interesting is that not a single song appeared in both top-5 lists. The system is doing its job of separating users with very different tastes, and it makes sense because energy is the most powerful numeric signal: rock songs score near zero for a chill listener, and lofi songs score near zero for a rock fan.

**Profile B (lofi/chill) vs Profile C (pop/happy)**

Both of these feel like "positive" or "feel-good" profiles, but they ended up with completely different results. Profile B got calm acoustic songs, while Profile C got bright energetic ones. Even though both users might be in a good mood, the energy target (0.38 vs 0.85) is so different that the scoring pulls their results apart. This is a good example of how the numeric features help separate users even when their mood labels sound similar.

**Profile C (pop/happy) vs Profile D (sad/energetic EDM)**

This comparison shows where the system breaks down. Profile C got Sunrise City at number one, which feels right for a happy pop fan. But Profile D, a user who said their mood is "sad," got Drop Zone, which is a euphoric EDM track. The reason is that Drop Zone's genre matched (edm) and that was worth 3.0 points, while the valence mismatch between a sad mood and a euphoric song only cost about 0.54 points. So the system recommended an emotionally wrong song because it was looking at genre identity more than emotional fit. A real person would find this recommendation strange.

**Profile D (sad/energetic) vs Profile F (acoustic rocker)**

Both of these are adversarial profiles, but they fail in slightly different ways. Profile D shows that genre can override emotional mood, while Profile F shows that genre can override a physical sound preference like acousticness. In both cases the genre and mood bonuses together create a ceiling that numeric features cannot break through. The difference is that Profile D's problem is about recommending the wrong feeling, and Profile F's problem is about recommending the wrong sound texture. Both point to the same root cause: the categorical weights are too strong relative to the numeric ones when the catalog is small.

**Profile A (rock/intense) vs Profile F (acoustic rocker)**

These two profiles have the same favorite genre and mood, but Profile F added likes_acoustic equal to True. Looking at the results, the top two songs are identical in both profiles (Storm Runner at number one, Gym Hero at number two), which means the acoustic preference had basically no effect on the ranking. This is the clearest evidence that the acousticness weight (1.0) is not strong enough to change outcomes when genre and mood already create such a large score advantage for the same songs.

---

### Why Gym Hero Keeps Showing Up for Happy Pop Users

Gym Hero is a workout pop song with a loud, intense feel, but it still shows up at number two for users who ask for happy pop music. The reason is that the scoring system only knows Gym Hero is a pop song, and matching the genre earns 3.0 points automatically. The system does not know the difference between "happy pop" and "gym pop" the way a human would. It sees that both are pop, gives Gym Hero the full genre bonus, and then ranks it above everything else that is not pop, even if those other songs feel more genuinely happy. The only thing stopping Gym Hero from being number one is that Sunrise City matches both genre and mood while Gym Hero only matches genre. This is a good example of how a scoring system can be technically correct but still feel off to a real listener.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

First, I would add more songs per genre. Right now 13 out of 15 genres have only one song, which means the genre bonus has nothing to compete against inside a genre. Adding even 3 or 4 songs per genre would let the numeric features like energy and acousticness actually matter for separating candidates.

Second, I would add an explicit valence preference to the user profile instead of guessing it from mood. The current approach uses a fixed lookup table, but the sad EDM test showed that mood and emotional valence are not always the same thing. Letting users say directly how happy or dark they want the music to feel would make the scoring more accurate for edge cases.

Third, I would add a diversity rule to the ranking step so the same genre or artist cannot appear more than twice in a top-5 list. Right now a lofi fan gets three lofi songs back to back, which is technically correct but does not expose them to anything new. A simple cap on repeating genres would make the results feel less like a filter bubble.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**What was your biggest learning moment during this project?**

My biggest learning moment was running the weight shift experiment. I expected that cutting the genre weight in half and doubling the energy weight would fix the problems I found in the adversarial profiles, but the rankings barely changed at all. That was the moment I realized the issue was never about the weights. It was about the catalog being too small. When only one rock song exists, Storm Runner will always win for a rock fan no matter what the weights say. I had been thinking about the problem the wrong way the whole time, and the experiment forced me to see that. Before I can tune weights meaningfully, I need more data.

**How did using AI tools help you, and when did you need to double-check them?**

AI tools helped me most during the design phase. When I was trying to figure out which features to include and how to weight them, being able to talk through the reasoning and see the math worked out step by step saved a lot of time. It also helped me catch the difference between features that look useful and features that actually discriminate, like how tempo and danceability seemed important at first but turned out to be redundant with energy in a small dataset.

The times I needed to double-check were when the suggestions sounded confident but I had not verified them against the actual data yet. For example, the valence lookup table was suggested based on what moods should feel like in general, but I had to manually check it against the actual song values in songs.csv to make sure the numbers made sense. Trusting the reasoning without checking the data would have meant building the scoring on assumptions instead of evidence.

**What surprised you about how simple algorithms can still "feel" like recommendations?**

I was genuinely surprised by how much the standard profiles felt right even though the logic is basically just addition and subtraction. When I ran the lofi listener profile and saw Library Rain, Midnight Coding, and Focus Flow come out as the top three in that exact order, it felt like the system actually understood something about that user. But looking at the code, it was just doing (1 - |gap|) times a weight for each feature. There is no understanding at all. It is just numbers that happen to line up with what a human would expect. That gap between what the output looks like and what is actually happening inside the code is probably the most important thing I learned from this whole project. It made me much more skeptical about trusting AI outputs in general just because they feel right.

**What would you try next if you extended this project?**

The first thing I would do is expand the catalog significantly, aiming for at least 5 to 10 songs per genre so the numeric features can actually separate candidates within a genre instead of just handing the win to the only available song. After that I would add an explicit valence field to the user profile so users can say directly how emotionally positive or dark they want the music to feel, rather than having the system guess from mood. I would also add a diversity rule to the ranking step so no genre appears more than twice in a top-5 list, which would reduce the filter bubble effect. And eventually I would love to try adding a simple collaborative filtering layer where the system looks at what other similar users listened to, not just the song features, to see if it could discover connections that pure content-based scoring would miss.
