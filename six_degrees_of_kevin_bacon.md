## Six Degrees of Kevin Bacon

### Story & Concept

The concepts measures how many steps it can take, from a person to another random person, outside
their known circle, By the chain of known persons.

These are called steps or degrees. As from the scientific data, we are connected to all people all
over the world by on average of _5-6 steps_, as the naming says six degrees.

the concept is highly beneficial, in terms of networking and connecting with people. Example: Get
a reference to apply for a job in a company, outside your known people.

- A fascinating explanation of the concept:
  <a href="https://www.youtube.com/watch?v=TcxZSmzPw8k"> Youtube Link </a>

### How to implement?

- **The Endpoint:** As similar to mutual_connections endpoint from objective 4, we will have the
`from_person` and we want to reach to `to_person`. We accept the ids of people, and output the
  degree and optionally the steps of people chain.

  - Eg. Endpoint route: `/connection/<person_id>/bacon_finder?target_id=<target_id>`

- **Model:**

    - Taking beacon it self, we create first query to filter `from_person_id` giving output to
    all available `to_person_id`.

    - Now we use the _all_ `to_person_id` id to filter above step, again.

    - We continue to do it until the _first connection_ that matches `from_person_id` to
    `to_person_id`. All the repetations of first query counted as steps. For recursive maybe we use
      `cte(recursive=True)`.

- **Challenges:**

    - Performance challenges can be common in the model. As we recursively filter queries, database
    with millions of users can hit the bandwidth/bottleneck limits. Potential solution would be to
      use concepts like Indexing, Caching and/or replicas for backups.


#### **Questions to ask business:**

- Output of the endpoint (Steps count, people chain, all possible chains)
- Approx. total users in database (for perf.)
